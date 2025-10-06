; NSIS Script for Selene Installer
; This script should be compiled on a Windows machine with NSIS installed.
; It assumes that the 'Selene.exe' executable has been built and is
; located in the '../dist' directory relative to this script.

;--------------------------------
; Application Details
;--------------------------------

!define APP_NAME "Selene"
!define APP_VERSION "1.0"
!define PUBLISHER "Selene Project"
!define EXE_NAME "Selene.exe"
!define INSTALLER_NAME "Selene_Installer.exe"
!define ICON_FILE "..\Functions\luna\Assets\icono.ico"
!define UNINSTALL_ICON_FILE "..\Functions\luna\Assets\icono.ico"

;--------------------------------
; Installer Configuration
;--------------------------------

; Name of the installer
OutFile "${INSTALLER_NAME}"

; Default installation directory
InstallDir "$PROGRAMFILES\${APP_NAME}"

; Set the icon for the installer
Icon "${ICON_FILE}"
UninstallIcon "${UNINSTALL_ICON_FILE}"

; Request admin privileges for installation
RequestExecutionLevel admin

;--------------------------------
; Pages
;--------------------------------

Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------
; Installation Section
;--------------------------------

Section "Install"

  ; Set output path to the installation directory
  SetOutPath $INSTDIR

  ; Add the main executable
  ; The file is expected to be in the 'dist' folder, one level up
  File "..\dist\${EXE_NAME}"

  ; Create the uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
; Uninstallation Section
;--------------------------------

Section "Uninstall"

  ; Remove files
  Delete "$INSTDIR\${EXE_NAME}"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove Start Menu shortcuts
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"

  ; Remove the installation directory
  RMDir "$INSTDIR"

SectionEnd