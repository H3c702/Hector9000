import QtQuick 2.11
//import QtQuick.Window 2.11
import QtQuick.Controls 2.0
//import QtQuick.VirtualKeyboard 2.3

Page {
    id: window
    visible: true
    width: 1024
    height: 600
    title: qsTr("Hector 9000 UI")

    ScreenView { anchors.fill: parent }

/*
    InputPanel {
        id: inputPanel
        z: 99
        x: 0
        y: window.height
        width: window.width

        states: State {
            name: "visible"
            when: inputPanel.active
            PropertyChanges {
                target: inputPanel
                y: window.height - inputPanel.height
            }
        }
        transitions: Transition {
            from: ""
            to: "visible"
            reversible: true
            ParallelAnimation {
                NumberAnimation {
                    properties: "y"
                    duration: 2500
                    easing.type: Easing.InOutQuad
                }
            }
        }
    }
*/
}
