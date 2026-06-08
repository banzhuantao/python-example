# python-example

## 使用到的外链

- [python](https://www.python.org/)
- [菜鸟教程-python3](https://www.runoob.com/python3/python3-tutorial.html)
- [streamlit](https://streamlit.io/)
- [ollama](https://ollama.com/)
- [pypi](https://pypi.org/)

---

## pyenv、python .zshrc 配置

```bash
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
export PYTHON_BUILD_MIRROR_URL=https://mirrors.ustc.edu.cn/python/
export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1
```


## 创建项目独立虚拟环境

```bash
# 创建环境
python -m venv .venv

# 激活环境(macos / linux)
source venv/bin/activate

# 安装 openai(只在当前项目生效)
pip install openai

# 退出虚拟环境
deactivate
```

---

## 生成依赖清单

```bash
pip freeze > requirements.txt
```

## 按照依赖清单下载项目虚拟环境依赖

```bash
pip install -r requirements.txt
```

---

## ollama 本机地址

`http://localhost:11434`

## Homebrew 安装的 Ollama

### 停止 Ollama

```bash
launchctl stop ollama
```

### 启动 Ollama

```bash
launchctl start ollama
```

### 重启

```bash
launchctl stop ollama && launchctl start ollama
```

### 强制停止所有 Ollama 进程

```bash
pkill -f ollama
```

### 重启 Ollama 后台运行, 不占用终端

```bash
nohup ollama serve &
```

### 前台启动

```bash
ollama serve
```

### 检查是否正常运行

```bash
curl http://localhost:11434/api/tags
```

有返回 JSON 就是正常启动。

### 设置开机自启 / 关闭自启

```bash
# 开机自启
launchctl enable ollama

# 关闭开机自启
launchctl disable ollama
```

---

robots.txt 查看规则

---


