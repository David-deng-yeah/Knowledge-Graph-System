
#npm list > npm_list.txt 2>&1
rm -rf __pycache__
git add -A *
auto_comment=`git status --short`
echo auto_comment=$auto_comment
git commit -m "$auto_comment"
git push ssh://$USER@$GITSVR/home/gitrepo/web.git master
git status
git gc
