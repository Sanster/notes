LFS 文件遗失，push 到新仓库时提示如下错误，push 失败：
```bash
LFS upload missing objects: (13/20), 200 MB | 0 B/s                                                                                                                                                                
  (missing) file1 (db8d9cf585d7b0037379853f504180a9c6fcb2410845d742f716cf82cd1d7a43)
  (missing) file2 (9380bea69e63639b9dab5c601c8fe99b64db4922bb67a19733680d232073290b)
```

设置允许不完整的 lfs object，然后 push
```bash
git config lfs.allowincompletepush 1
```
