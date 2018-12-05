import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Extras 1.4

Item {
    width: 800
    height: 80

    DarkBackground {
        id: nackground
        anchors.fill: parent

        Label {
            id: messageLabel
            y: 21
            color: "#ffffff"
            text: screenManager.status
            anchors.verticalCenterOffset: 0
            anchors.left: parent.left
            anchors.leftMargin: 25
            anchors.verticalCenter: parent.verticalCenter
            font.pointSize: 32
            font.family: "Tahoma"
        }

        ProgressBar {
            id: progressBar
            x: 499
            y: 43
            width: 200
            height: 29
            anchors.right: parent.right
            anchors.rightMargin: 25
            anchors.verticalCenter: parent.verticalCenter
            wheelEnabled: false
            to: 100
            value: screenManager.barValue
        }
    }
}
