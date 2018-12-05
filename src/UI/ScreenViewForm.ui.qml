import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.4

Item {
    width: 1024
    height: 600

    ColumnLayout {
        id: column0
        anchors.fill: parent
        spacing: 0

        HecToolBar {
            id: topBar
            Layout.maximumHeight: 80
            Layout.minimumHeight: 80
            Layout.preferredHeight: 80
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            height: 80
            z: 2
        }
        DarkBackground {
            id: rectangle
            width: 200
            height: 200
            color: "#ffffff"
            Layout.fillHeight: true
            Layout.fillWidth: true

            LightBackground {
                id: alertBox
                visible: screenManager.alertVisible
                x: 256
                y: 20
                width: 512
                height: 400
                color: "#ffffff"
                z: 3

                Text {
                    id: text1
                    color: "#ffffff"
                    text: screenManager.alert
                    wrapMode: Text.WordWrap
                    anchors.left: parent.left
                    anchors.leftMargin: 32
                    font.family: "Verdana"
                    font.bold: true
                    anchors.top: parent.top
                    anchors.topMargin: 96
                    anchors.right: parent.right
                    anchors.rightMargin: 32
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 96
                    font.pixelSize: 42
                }

                Button {
                    id: okbutton
                    x: 206
                    y: 352
                    text: qsTr("OK")
                    visible: screenManager.alertButtonVisible
                    //onClicked:
                }
            }

            ButtonMenu {
                id: contentArea
                visible: screenManager.buttonMenuVisible
                anchors.fill: parent
                Layout.fillWidth: true
                Layout.fillHeight: true
                z: 1
            }

            Dispensing {
                visible: screenManager.dispensingVisible
            }
        }
        StatusBar {
            id: bottomBar
            Layout.maximumHeight: 80
            Layout.minimumHeight: 80
            Layout.preferredHeight: 80
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
            height: 80
            z: 2
        }
    }
}
