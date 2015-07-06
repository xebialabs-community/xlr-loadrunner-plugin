# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS. 
import sys

from java.lang import Exception
from java.io import PrintWriter
from java.io import StringWriter

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily, Overthere
from com.xebialabs.overthere.cifs import CifsConnectionBuilder
from com.xebialabs.overthere.cifs import CifsConnectionType
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils

class QtpCScript():
    def __init__(self, username, password, address, connectionType, timeout, allowDelegate, WlrunExe, TestPath, ResultName):
        self.options = ConnectionOptions()
        self.options.set(ConnectionOptions.USERNAME, username)
        self.options.set(ConnectionOptions.PASSWORD, password)
        self.options.set(ConnectionOptions.ADDRESS, address)
        self.options.set(ConnectionOptions.OPERATING_SYSTEM, OperatingSystemFamily.WINDOWS)

        self.TestPath = TestPath
        self.ResultName = ResultName
        self.connectionType = connectionType
        # WINRM_NATIVE only
        self.allowDelegate = allowDelegate
        # WINRM_INTERNAL only
        self.timeout = timeout
        
        self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
        self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

    def customize(self, options):
        if self.connectionType == 'WINRM_NATIVE':
            options.set(CifsConnectionBuilder.CONNECTION_TYPE, CifsConnectionType.WINRM_NATIVE)
            options.set(CifsConnectionBuilder.WINRS_ALLOW_DELEGATE, allowDelegate)
        elif self.connectionType == 'WINRM_INTERNAL':
            options.set(CifsConnectionBuilder.CONNECTION_TYPE, CifsConnectionType.WINRM_INTERNAL)
            options.set(CifsConnectionBuilder.WINRM_KERBEROS_USE_HTTP_SPN, True)
            options.set(CifsConnectionBuilder.WINRM_TIMEMOUT, timeout);
        #print 'DEBUG: Options:', options

    def execute(self):
        self.customize(self.options)
        connection = None
        try:
            connection = Overthere.getConnection(CifsConnectionBuilder.CIFS_PROTOCOL, self.options)
            connection.setWorkingDirectory(connection.getFile(self.TestPath))
            # upload the ResultName and pass it to csResultName.exe
            ResultNameCommand = CmdLine.build(WlrunExe, "-Run", "-TestPath", TestPath, "-ResultName", ResultName)
            return connection.execute(self.stdout, self.stderr, ResultNameCommand)
        except Exception, e:
            stacktrace = StringWriter()
            writer = PrintWriter(stacktrace, True)
            e.printStackTrace(writer)
            self.stderr.handleLine(stacktrace.toString())
            return 1
        finally:
            if connection is not None:
                connection.close()

    def getStdout(self):
        return self.stdout.getOutput()

    def getStdoutLines(self):
        return self.stdout.getOutputLines()

    def getStderr(self):
        return self.stderr.getOutput()

    def getStderrLines(self):
        return self.stderr.getOutputLines()

ResultName = QtpCScript(username, password, address, connectionType, timeout, allowDelegate, WlrunExe, TestPath, ResultName)
exitCode = ResultName.execute()

output = ResultName.getStdout()
err = ResultName.getStderr()

if (exitCode == 0):
    print output
else:
    print "Exit code "
    print exitCode
    print
    print "#### Output:"
    print output

    print "#### Error stream:"
    print err
    print
    print "----"

    sys.exit(exitCode)

