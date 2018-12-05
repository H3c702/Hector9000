import QtQuick 2.4
import QtQuick.Controls 2.4

Item {
    id: buttonMenuContainer
    width: 1024
    height: 440

    GridView {
        id: gridView
        width: 974
        layoutDirection: Qt.LeftToRight
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.top: parent.top
        clip: false
        keyNavigationWraps: true
        opacity: 1
        flickableDirection: Flickable.VerticalFlick
        snapMode: GridView.SnapOneRow

        property int idealCellHeight: height / 2
        property int idealCellWidth: height / 2
        cellHeight: idealCellHeight
        cellWidth: width / Math.floor(width / idealCellWidth)

        delegate: Item {
            id: item1
            height: GridView.view.cellHeight
            width: GridView.view.cellWidth

            RoundButton {
                id: rect
                radius: 15
                anchors.centerIn: parent
                width: parent.GridView.view.idealCellWidth - 20
                height: parent.height - 20
                palette.button: colorCode
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
        }

        model: menuModel
    }
}
