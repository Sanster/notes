一定程度上缓解 GPU memory inbanlance 问题：https://discuss.pytorch.org/t/dataparallel-imbalanced-memory-usage/22551

把 gt 和模型的输出放在单独的一块卡上
```
export CUDA_VISIBLE_DEVICES=0,1,2,3
calling model = DataParallel(model, device_ids=[0,1,2], output_device=3).cuda() 
gt = gt.cuda(3)
pred = calling_model(input)
```
