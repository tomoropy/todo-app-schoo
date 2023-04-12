# WEB アプリケーション開発入門

Python を使って ToDo アプリを作って、基本的なアプリケーションの仕組みを学ぼう

## 利用技術

- python
- flask
- MySQL
- Docker
- docker-compose

## 説明

第 3 回 環境構築をしよう → hello-world ブランチ  
第 4 回 User の処理を実装しよう → login ブランチ  
第 5 回 Task の処理を実装しよう → task ブランチ

## 環境構築方法

```
$ git clone https://github.com/tomoropy/todo-app-schoo.git
```

特定のブランチをクローンする方法

```
$ git clone -b [ブランチ名] https://github.com/tomoropy/todo-app-schoo.git
```

Docker-compose がない場合は事前にダウンロードしてください

```
$ docker-compose up
```

Error になる場合(db を立ち上げたあとで、別ターミナルで app を立ち上げる)

```
$ docker-compose up db
```

```
$ docker-compose up app
```
