# README

For this custom projects, We use raw git on ssh, i.e. not gitlab or other git server needed...

# WARNING

NEVER use root directly UNLESS you are aware of the reason !!!

# setup

## git config
git config --global user.email "$USER@local"
git config --global user.name "$USER@local"

## add gitsvr to bashrc and test

```
echo export GITSVR=10.94.81.132 >> ~/.bashrc
bash
echo GITSVR=$GITSVR
```

## git clone to local

git clone ssh://$USER@$GITSVR/home/gitrepo/web.git

## push to remote with your linux acct

git push ssh://$USER@$GITSVR/home/gitrepo/web.git master

# data flow

## neo4j

```
gbase (raw data from custom)
    => mysql (data-science-db) by zhouzhou
    => .pkl (python read db and dump to pkl) from /home/gitrepo/dragon
    => py scripts to import to neo4j
    => neo4j (py by team XXX) => neo4j.py
    => web
```





# test2

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

# knowledge-graph-system
