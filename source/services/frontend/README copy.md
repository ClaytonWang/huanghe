# 前端项目模板

## 构建
```bash
npm ci
npm build
```

## 开发/启动
```bash
npm ci
npm run mock // 当webpack.dev.config.js文件中，mock为true时，启动本地mock服务。如果mock为false，无需执行该命令。
npm start
```

## 代码提交
### 前置条件
vscode安装eslint插件
安装eslint和prettier
```bash
npm install -g eslint
npm install -g prettier
```
### 提交
```bash
npm run lint
```
代码提交之前，本地通过npm run lint检查代码格式，以及自动修正和格式化代码风格。
npm commit时，先出发pre-commit进行代码校验和修正，同时校验commit message格式。
commit message支持'build', 'chore', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'revert', 'style', 'test'格式，详细：
https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/index.js

## cicd

## 技术栈
- react 18
- react-router-dom 6
- antd 4
- webpack 5
