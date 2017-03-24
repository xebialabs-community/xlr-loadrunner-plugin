# XL Release HP LoadRunner Plugin #

## Introduction: ##
This plugin will allow you to execute HP LoadRunner scenarios from XL Release.  A report with the test results will be returned to XL Release.

## CI status ##

[![Build Status][xlr-loadrunner-plugin-travis-image] ][xlr-loadrunner-plugin-travis-url]
[![Codacy][xlr-loadrunner-plugin-codacy-image] ][xlr-loadrunner-plugin-codacy-url]
[![Code Climate][xlr-loadrunner-plugin-code-climate-image] ][xlr-loadrunner-plugin-code-climate-url]
[![License: MIT][xlr-loadrunner-plugin-license-image] ][xlr-loadrunner-plugin-license-url]


[xlr-loadrunner-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-loadrunner-plugin.svg?branch=master
[xlr-loadrunner-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-loadrunner-plugin
[xlr-loadrunner-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/05421387f40b4e93bed72cecf0dd43e3
[xlr-loadrunner-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xlr-loadrunner-plugin
[xlr-loadrunner-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-loadrunner-plugin/badges/gpa.svg
[xlr-loadrunner-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-loadrunner-plugin
[xlr-loadrunner-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-loadrunner-plugin-license-url]: https://opensource.org/licenses/MIT


## Installation: ##
Copy the plugin file to the XL Release plugin folder and restart the XL Release server. 

## Configuring an Example Template: ##
The Load Runner plugin provides one new task (Hp Tools: Run Load Runner).  You can add this step to you release template.

![image](images/pluginList.png)

You can configure this task as follows:

![image](images/TaskConfig_1.png)

The first few properties (Username, Password, Address, Connection Type and Timeout) are for configuring the connection to the remote host where QTP or UFT is installed.

![image](images/TaskConfig_2.png) 

Then we can configure the Test Path to point to the directory on the remote host where the test configuration is.  You can also configure the timeouts.  You should take care to make sure that you choose your timeouts wisely to ensure that the tests or the connection to the remote host don’t timeout before the load test is complete.

![image](images/DemoRelease.png) 

Once the release has been started and the Run QTP task is executing you can verify the test are running by looking for the UFT process in the Windows Task Manager as follows:
 
![image](images/TaskManager.png)

If the tests execute quickly you may not see the processes.  In any event since the tests are not automated via XL Release there is no need for a Window to display the progress of the tests.  Once the QTP step of the release has been completed the results of the test will be available in the output of the XL Release task as follows:

![image](images/FinishedTask.png) 

It this example we have 2 tests, one failed and the other succeeded.
 

 ## Notice ##

 This plugin uses parts of the Jenkins plugin hp-application-automation-tools-plugin to execute tests on a Load Runner server.  Details about the Jenkins plugin can be found at [JENKINS/HP+Application+Automation+Tools](https://wiki.jenkins-ci.org/display/JENKINS/HP+Application+Automation+Tools)

 The copywrite notice for the Jenkins components (i.e. HpToolsLauncher.exe) is as follows:

(c) Copyright 2012 Hewlett-Packard Development Company, L.P. 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
