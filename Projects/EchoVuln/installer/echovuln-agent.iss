#define MyAppName       "EchoVuln Agent"
#define MyAppPublisher  "EchoPentest"
#define MyAppVersion    "2.0.0"
#define MyServiceName   "EchoVulnAgent"

[Setup]
AppId={{A4E6F7B3-6E0D-4C6E-9A6A-1F5C8C9D3B21}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf64}\EchoPentest\EchoVulnAgent
DisableProgramGroupPage=yes
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
OutputDir=.\out
OutputBaseFilename=EchoVulnAgent-Setup-{#MyAppVersion}
UninstallDisplayIcon={app}\agent\echovuln-agent.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: startsvc; Description: "Start EchoVuln Agent service after install"; Flags: checkedonce

[Files]
; PyInstaller one-dir output
Source: "..\dist\echovuln-agent\*"; \
  DestDir: "{app}\agent"; \
  Flags: recursesubdirs createallsubdirs ignoreversion

; NSSM service wrapper
Source: "..\thirdparty\nssm.exe"; \
  DestDir: "{commonappdata}\EchoPentest\EchoVuln\agent"; \
  Flags: ignoreversion

[UninstallRun]
Filename: "{commonappdata}\EchoPentest\EchoVuln\agent\nssm.exe"; \
  Parameters: "stop {#MyServiceName}"; Flags: runhidden
Filename: "{commonappdata}\EchoPentest\EchoVuln\agent\nssm.exe"; \
  Parameters: "remove {#MyServiceName} confirm"; Flags: runhidden

[Code]
var
  BackendUrlPage: TInputQueryWizardPage;
  EnrollKeyPage: TInputQueryWizardPage;

function PdDir(): string;
begin
  Result := ExpandConstant('{commonappdata}') + '\EchoPentest\EchoVuln\agent';
end;

function NssmPath(): string;
begin
  Result := PdDir() + '\nssm.exe';
end;

function AgentExePath(): string;
begin
  Result := ExpandConstant('{app}') + '\agent\echovuln-agent.exe';
end;

procedure InitializeWizard;
begin
  BackendUrlPage := CreateInputQueryPage(
    wpWelcome,
    'Backend URL',
    'EchoVuln backend address',
    'Enter the backend base URL (example: https://vuln.yourdomain.com).'
  );
  BackendUrlPage.Add('Backend URL:', False);
  BackendUrlPage.Values[0] := 'http://127.0.0.1:8000';

  EnrollKeyPage := CreateInputQueryPage(
    BackendUrlPage.ID,
    'Enroll Key',
    'Agent enrollment key',
    'Paste the enroll key (ek_...). This is required only once.'
  );
  EnrollKeyPage.Add('Enroll Key:', False);
  EnrollKeyPage.Values[0] := '';
end;

function Quote(const S: string): string;
begin
  Result := '"' + S + '"';
end;

function BuildServiceArgs(): string;
begin
  Result := '--backend-url ' + Quote(BackendUrlPage.Values[0]);
  if Trim(EnrollKeyPage.Values[0]) <> '' then
    Result := Result + ' --enroll-key ' + Quote(Trim(EnrollKeyPage.Values[0]));
end;

procedure EnsurePdDir();
begin
  if not DirExists(PdDir()) then
    ForceDirectories(PdDir());
end;

procedure RunNssm(const Params: string);
var
  Rc: Integer;
begin
  if not Exec(NssmPath(), Params, PdDir(), SW_HIDE, ewWaitUntilTerminated, Rc) then
  begin
    MsgBox('Failed to execute NSSM', mbCriticalError, MB_OK);
    Abort;
  end;

  if Rc <> 0 then
  begin
    MsgBox('NSSM failed (exit ' + IntToStr(Rc) + '): ' + Params, mbCriticalError, MB_OK);
    Abort;
  end;
end;

procedure InstallService();
var
  Rc: Integer;
begin
  EnsurePdDir();


  Exec(NssmPath(), 'stop {#MyServiceName}', PdDir(), SW_HIDE, ewWaitUntilTerminated, Rc);
  Exec(NssmPath(), 'remove {#MyServiceName} confirm', PdDir(), SW_HIDE, ewWaitUntilTerminated, Rc);

  RunNssm(
    'install {#MyServiceName} ' +
    Quote(AgentExePath()) + ' ' +
    BuildServiceArgs()
  );

  RunNssm('set {#MyServiceName} AppDirectory ' + Quote(ExpandConstant('{app}') + '\agent'));
  RunNssm('set {#MyServiceName} Start SERVICE_AUTO_START');

  RunNssm('set {#MyServiceName} AppStdout ' + Quote(PdDir() + '\service_stdout.log'));
  RunNssm('set {#MyServiceName} AppStderr ' + Quote(PdDir() + '\service_stderr.log'));
  RunNssm('set {#MyServiceName} AppRotateFiles 1');
  RunNssm('set {#MyServiceName} AppRotateOnline 1');
  RunNssm('set {#MyServiceName} AppRotateSeconds 86400');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    InstallService();
    if IsTaskSelected('startsvc') then
      RunNssm('start {#MyServiceName}');
  end;
end;
