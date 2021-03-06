#!/usr/bin/env python3

"""
Use touch events to drag a rectangle around the screen with borders,
keeping the rectangle inside a specified widget and keeping the
rectangle from sliding away from the touch position when going in and
out of the specified widget's screen area.  The rectangle is also only
allowed to be dropped in the area of a specified widget.
"""

from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

kv = """
<Rect>:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.x,self.y

<DragRect>:
    drag_rectangle: self.x, self.y, self.width, self.height

<MyLabel>:
    background_color: 0.5,0.5,0.5,1
    color: 0,0,0,1
    padding: 10, 10

<Box>:
    pos: 100, 100
    size_hint: None, None
    size: 50,50
    background_color: 0,1,0,0.5

BoxLayout:
    orientation: "horizontal"
    MyLabel:
        text: "Left"
        size_hint_x: None
        width: self.texture_size[0]
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            id: drag_area
            orientation: "vertical"
            MyLabel:
                text: "Drag over me"
                size_hint_y: None
                height: 100
                background_color: 1.0,0,0,1
            RelativeLayout:
                id: page
                Box:
                    drag_area: drag_area
                    pos: 100, 200
                    background_color: 0,0,1,0.5
        MyLabel:
            text: "Bottom"
            size_hint_y: None
            height: self.texture_size[1]
    MyLabel:
        text: "Right"
        size_hint_x: None
        width: self.texture_size[0]
"""

# mixin class
class Rect:
    background_color = ListProperty([1, 1, 1, 1])

# Similar to DragBehavior
class DragRect(Rect, FloatLayout):
    drag_area = ObjectProperty(None)
    drop_area = ObjectProperty(None)
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._x_offset = 0
        self._y_offset = 0
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self._x_offset = self.x - touch.x
            self._y_offset = self.y - touch.y
            return True # Don't allow simultaneous grabs
        
    def on_touch_move(self, touch):
        if not touch.grab_current is self:
            return

        self.x = touch.x + self._x_offset
        self.y = touch.y + self._y_offset

        # Stay inside drag_area widget    
        self.move_inside(self.drag_area)
                
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # Stay inside drop_area widget
            self.move_inside(self.drop_area)

            touch.ungrab(self)

    def move_inside(self, widget):
        if widget is None:
            widget = self.parent

        if self.x < 0:
            self.x = 0
        elif self.right > widget.width:
            self.right = widget.width

        if self.y < 0:
            self.y = 0
        elif self.top > widget.height:
            self.top = widget.height
        
class RectLabel(Rect, Label):
    pass

class MyLabel(RectLabel):
    pass

class Box(DragRect):
    pass

class TestApp(App):
    def build(self):
        root = Builder.load_string(kv)
        page = root.ids.page
        page.add_widget(Box())
        return root
    
TestApp().run()
