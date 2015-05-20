# fixxd
iOS UIAutomation tests launcher

#installation
```
pip install fixxd
```

Go in the folder you want to put the tests in:
```
echo "app_name:MyApp.app" > .fixxd
mkdir iphone
mkdir lib
```
#usage
Put your tests in the `iphone`, `ipad` or `universal` folder.
Put your lib / utils in the `lib` folder.

Then run `fixxd test iphone/mytest.coffee`

#contributing
TODO

# thanks
This library is inspired by both [ui-automation-runner](https://github.com/idStar/ui-automation-runner/) and [bwoken](https://github.com/bendyworks/bwoken). Thanks to them.
