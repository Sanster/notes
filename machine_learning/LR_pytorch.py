"""
https://medium.com/jovian-io/image-classification-using-logistic-regression-in-pytorch-ebb96cc9eb79
"""

import torch
from torch import nn
import torch.nn.functional as F
import torchvision
from torchvision.datasets import MNIST
from torchvision.transforms import transforms
from torch.utils.data.sampler import SubsetRandomSampler
from torch.utils.data.dataloader import DataLoader

import numpy as np


class MnistModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, num_classes)
        self.log_sigmoid = nn.LogSigmoid()

    def forward(self, input):
        input = input.reshape(-1, input_size)
        out = self.linear(input)
        out = self.log_sigmoid(out)
        return out


batch_size = 100
input_size = 28 * 28
num_classes = 10
learning_rate = 0.001

model = MnistModel()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
loss_fn = nn.NLLLoss()


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.sum(preds == labels).item() / len(preds)


def split_indices(n, val_pct):
    n_val = int(val_pct * n)
    idxs = np.random.permutation(n)
    return idxs[n_val:], idxs[:n_val]


def loss_batch(model, loss_func, xb, yb, opt=None, metric=None):
    preds = model(xb)
    loss = loss_func(preds, yb)

    if opt is not None:
        loss.backward()
        opt.step()
        opt.zero_grad()

    metric_result = None
    if metric is not None:
        metric_result = metric(preds, yb)

    return loss.item(), len(xb), metric_result


def evaluate(model, loss_fn, valid_dl, metric=None):
    with torch.no_grad():
        results = [loss_batch(model, loss_fn, xb, yb, metric=metric) for xb, yb in valid_dl]
        losses, nums, metrics = zip(*results)
        total = np.sum(nums)
        total_loss = np.sum(np.multiply(losses, nums))
        avg_loss = total_loss / total
        avg_metric = None
        if metric is not None:
            tot_metric = np.sum(np.multiply(metrics, nums))
            avg_metric = tot_metric / total
    return avg_loss, total, avg_metric


def fit(epochs, model, loss_fn, opt, train_dl, valid_dl, metric=None):
    for epoch in range(epochs):
        for xb, yb in train_dl:
            loss, _, _ = loss_batch(model, loss_fn, xb, yb, opt)

        result = evaluate(model, loss_fn, valid_dl, metric)
        val_loss, total, val_metric = result

        if metric is None:
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, epochs, val_loss))
        else:
            print('Epoch [{}/{}], Loss: {:.4f}, {}: {:.4f}'.format(epoch + 1,
                                                                   epochs,
                                                                   val_loss,
                                                                   metric.__name__,
                                                                   val_metric))


if __name__ == "__main__":
    dataset = MNIST(root='data/',
                    download=True,
                    transform=transforms.ToTensor())

    train_indices, val_indices = split_indices(len(dataset), 0.2)
    print("Train dataset size:", len(train_indices))
    print("Val dataset size:", len(val_indices))

    train_sampler = SubsetRandomSampler(train_indices)
    train_loader = DataLoader(dataset,
                              batch_size,
                              sampler=train_sampler)

    val_sampler = SubsetRandomSampler(val_indices)
    val_loader = DataLoader(dataset,
                            batch_size,
                            sampler=val_sampler)

    test_dataset = MNIST(root='data/', train=False)
    print("Test dataset size:", len(test_dataset))

    fit(9, model, F.cross_entropy, optimizer, train_loader, val_loader, accuracy)
