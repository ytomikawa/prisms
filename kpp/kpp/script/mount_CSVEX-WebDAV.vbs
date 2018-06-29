' ���[�UID�E�p�X���[�h�i�uYOUR-ID�v�uYOUR-PASSWORD�v�͗v�ύX�A�u"�v�͎c�����Ɓj
Dim UserID, Password
UserID = "shin"
Password = "Ws97k3S6"

' �h���C�u������i�g�p���Ă��Ȃ��C�ӂ̃h���C�u�ɕύX�\�j
Dim Drive
Drive = "y:"

' ���L�t�H���_�iWebDAV�j�ݒ���
Dim WebDAV, DriveName
WebDAV = "https://secure6216m.sakura.ne.jp:9802/csvex/webdav/"
DriveName = "CSVEX-WebDAV"


' ���L�t�H���_�iWebDAV�j�̃}�E���g
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

If objFSO.DriveExists(Drive) = False Then
	Set objNetwork = CreateObject("WScript.Network")
	objNetwork.MapNetworkDrive Drive, WebDAV, False, UserID, Password
	
	Set objShell = CreateObject("Shell.Application")
	objShell.NameSpace(Drive & "\").Self.Name = DriveName
	
	MsgBox("���L�t�H���_�iWebDAV�j�𐳏�Ƀ}�E���g���܂����B" & vbCr & vbCr & "�y�Ώہz" & vbCr & objShell.NameSpace(Drive & "\").Self.Name)
Else
	Set objShell = CreateObject("Shell.Application")
	MsgBox("�w�肳�ꂽ�h���C�u�͊��Ƀ}�E���g����Ă��܂��B" & vbCr & "�}�E���g�����𒆒f���܂����B" & vbCr & "�X�N���v�g��̃h���C�u�������ύX���čēx���s���ĉ������B" & vbCr & vbCr & "�y�Ώہz" &	vbCr & objShell.NameSpace(Drive & "\").Self.Name)
End If
