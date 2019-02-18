import QtQuick 2.4
import QtQuick.Controls 2.0
import QtQuick.Extras 1.4

Item {
    width: 800
    height: 80

    DarkBackground {
        id: background
        anchors.fill: parent

        Label {
            id: titleLabel
            x: -2
            y: 19
            color: "#ffffff"
            text: screenManager.title
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            font.pointSize: 32
            font.family: "Tahoma"
            font.bold: true
            anchors.verticalCenterOffset: 0
        }

        Image {
            id: image
            x: 707
            y: 8
            width: 43
            height: 45
            anchors.right: parent.right
            anchors.rightMargin: 25
            anchors.verticalCenter: parent.verticalCenter
            source: "../img/icon-settings.png"
        }

        Image {
            id: image1
            y: 0
            width: 192
            height: 80
            anchors.left: parent.left
            anchors.leftMargin: 25
            anchors.verticalCenter: parent.verticalCenter
            fillMode: Image.PreserveAspectFit
            source: "../img/H9k.png"
        }
    }
}

/*##^## Designer {
    D{i:5;anchors_x:0}
}
 ##^##*/
