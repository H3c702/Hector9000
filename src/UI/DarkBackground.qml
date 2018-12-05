import QtQuick 2.0
import QtQuick.Controls.Styles 1.1

Rectangle {
    property bool pressed: false
    color: "#000000"

    gradient: Gradient {
        GradientStop {
            position: 0
            color: "#000000"
        }
        GradientStop {
            color: "#222"
            position: 1
        }
    }
    Rectangle {
        height: 1
        width: parent.width
        anchors.top: parent.top
        color: "#444"
        visible: !pressed
    }
    Rectangle {
        height: 1
        width: parent.width
        anchors.bottom: parent.bottom
        color: "#000"
    }
}
