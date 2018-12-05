import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Extras 1.4

Item {
    id: dispensingContainer
    width: 1024
    height: 440

    Image {
        id: image
        width: 350
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 45
        anchors.top: parent.top
        anchors.topMargin: 45
        anchors.left: parent.left
        anchors.leftMargin: 45
        fillMode: Image.PreserveAspectFit
        source: "../img/empty-glass.png"

        BusyIndicator {
            id: busyIndicator
            x: 145
            y: 88
            running: false
        }

        Gauge {
            id: gauge
            x: 0
            y: 66
            width: 56
            height: 276
            value: screenManager.gaugeValue
        }
    }

    GridView {
        id: grid
        x: 400
        y: 20
        width: 600
        height: 400
        cellHeight: 200

        //spacing: 0
        //rows: 2
        //columns: 6
        model: dispensingModel
        delegate: Item {
            id: item1
            height: GridView.view.cellHeight
            width: GridView.view.cellWidth

            Image {
                id: channelImg
                width: 100
                height: 175
                fillMode: Image.PreserveAspectCrop
                source: "../img/bottle.png"

                Label {
                    id: channelId
                    x: 11
                    y: 175
                    width: 70
                    height: 16
                    color: channelColor
                    text: channelName
                    horizontalAlignment: Text.AlignHCenter
                }

                StatusIndicator {
                    id: statusIndicator1
                    x: 24
                    y: 75
                    width: 45
                    height: 45
                    active: true
                    color: indicatorColor
                }
            }


            /**
            RoundButton {
                id: rect
                radius: 15
                anchors.centerIn: parent
                width: parent.GridView.view.idealCellWidth - 20
                height: parent.height - 20
                //palette.button: colorCode
                onClicked: menuManager.clickedId = menuId
            }

            Text {
                property color rectCol: colorCode
                color: ((rectCol.hslLightness > 0.5) ? "black" : "white")
                //color: ((rectCol.hsvValue > 0) ? "black" : "white")
                anchors.centerIn: parent
                text: name
                font.bold: true
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }
**/
        }
    }

    Label {
        id: label
        color: "#ffffff"
        text: screenManager.contentValue
        anchors.right: image.right
        anchors.rightMargin: 0
        anchors.left: image.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.top: image.bottom
        anchors.topMargin: 5
        font.family: "Tahoma"
        font.bold: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.pointSize: 27
    }
}


/*##^## Designer {
    D{i:1;anchors_height:350;anchors_width:350;anchors_x:45;anchors_y:45}D{i:13;anchors_x:8;anchors_y:405}
}
 ##^##*/
