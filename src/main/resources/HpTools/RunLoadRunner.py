# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS. 
import sys
import java.lang.System as System
import java.text.SimpleDateFormat as Sdf
import java.sql.Date as Date


from java.lang import Exception
from java.io import PrintWriter
from java.io import StringWriter
from java.lang import ClassLoader

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily, Overthere
from com.xebialabs.overthere.cifs import CifsConnectionBuilder
from com.xebialabs.overthere.cifs import CifsConnectionType
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils

class WinrmRemoteHpTools():
    def __init__(self, username, password, address, connectionType, timeout, allowDelegate, remotePath, script):
        self.options = ConnectionOptions()
        self.options.set(ConnectionOptions.USERNAME, username)
        self.options.set(ConnectionOptions.PASSWORD, password)
        self.options.set(ConnectionOptions.ADDRESS, address)
        self.options.set(ConnectionOptions.OPERATING_SYSTEM, OperatingSystemFamily.WINDOWS)

        self.remotePath = remotePath
        self.script = script
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
            connection.setWorkingDirectory(connection.getFile(self.remotePath))
            # upload the script and pass it to cscript.exe
            targetFile = connection.getTempFile('parameters', '.txt')
            OverthereUtils.write(String(self.script).getBytes(), targetFile)
            targetFile.setExecutable(True)
            exeFile = connection.getTempFile('HpToolsLauncher', '.exe')
            sysloader = ClassLoader.getSystemClassLoader()
            OverthereUtils.write(sysloader.getResourceAsStream("HpTools/HpToolsLauncher.exe"), exeFile)
            exeFile.setExecutable(True)
            # run cscript in batch mode
            scriptCommand = CmdLine.build(exeFile.getPath(), '-paramfile', targetFile.getPath())
            return connection.execute(self.stdout, self.stderr, scriptCommand)
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

myDate = Date(System.currentTimeMillis())
df = Sdf('yyyyMMddyyHHMMss')
dt = df.format(myDate)
testPath = testPath.replace( "\\", "\\\\")
testPath = testPath.replace( "\:", "\\\:")
paramfile = """
# Demo Parameters file
#
Test1=%s
resultsFilename=Results%s.xml
runType=FileSystem
PerScenarioTimeOut=%s
controllerPollingInterval=%s
fsTimeout=%s
""" % (testPath, dt, PerScenarioTimeout, controllerPolliingInterval, fsTimeout)



script = WinrmRemoteHpTools(username, password, address, connectionType, timeout, allowDelegate, remotePath, paramfile)
exitCode = script.execute()

output = script.getStdout()
err = script.getStderr()

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

    #sys.exit(exitCode)
    sys.exit(0)

