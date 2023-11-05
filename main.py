import sys
import io
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from random import choice

NUMBER = ['1', '2', '3', '4', '5', '6', '7', '7', '8', '9', '0']  # цифирки

SLOTS_TYPES = ['7', '7', '7', 'bar', 'bar', 'bar', 'bar', 'bar',  # 8
               'b', 'b', 'b', 'b', 'b', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'g',  # 13
               'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'c', 'c', 'c',  # 11
               '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']  # 18
# 32/50 удачных слотов


TROLL_PHRASES = ['Сегодня не твой день', 'Неудачник', 'Деньги - прощайте',
                 'Банкротство - здравствуй', 'На улице тоже есть чем питаться',
                 'Может в другой раз повезёт', 'Терпи', 'Неповезло(',
                 'Ещё одна неудача', 'Какой же позор!']  # при проигрыше

VICTORY_PHRASES = ['И у нас победитель!', 'Мне кажется ты жульничал',
                   'Кто бы мог поверить?!', 'Jackpot!!!', 'Судьба тебя одарила']  # при выйгрыше

SLOT_PICTURE = {'c': 'Cherry_slot.png', '7': 'Seven_slot.png', 'bar': 'Bar_slot.png', 'b': 'bell_slot.png',
                'g': 'Grape_slot.png', 'l': 'Lemon_slot.png', '.': 'Empty_slot.png'}

casino_project = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>651</width>
    <height>781</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Казино</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="start_layout" native="true">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>651</width>
      <height>761</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true"/>
    </property>
    <widget class="QPushButton" name="register_button">
     <property name="geometry">
      <rect>
       <x>240</x>
       <y>220</y>
       <width>171</width>
       <height>81</height>
      </rect>
     </property>
     <property name="focusPolicy">
      <enum>Qt::WheelFocus</enum>
     </property>
     <property name="text">
      <string>Зарегистрироваться</string>
     </property>
    </widget>
    <widget class="QPushButton" name="enter_button">
     <property name="geometry">
      <rect>
       <x>240</x>
       <y>320</y>
       <width>171</width>
       <height>81</height>
      </rect>
     </property>
     <property name="text">
      <string>Войти</string>
     </property>
     <property name="iconSize">
      <size>
       <width>16</width>
       <height>16</height>
      </size>
     </property>
    </widget>
    <widget class="QLabel" name="pict1">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>651</width>
       <height>761</height>
      </rect>
     </property>
     <property name="text">
      <string/>
     </property>
    </widget>
    <zorder>pict1</zorder>
    <zorder>register_button</zorder>
    <zorder>enter_button</zorder>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources>
  <include location="../../Desktop/Fon1.qrc"/>
 </resources>
 <connections/>
</ui>"""

casino_project2 = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>651</width>
    <height>781</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Казино</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="register_layout" native="true">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>661</width>
      <height>761</height>
     </rect>
    </property>
    <property name="acceptDrops">
     <bool>false</bool>
    </property>
    <widget class="QLabel" name="label">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>60</y>
       <width>201</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:14pt;&quot;&gt;
      Введите новый логин:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="label_2">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>200</y>
       <width>211</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:14pt;&quot;&gt;
      Введите новый пароль:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="label_3">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>340</y>
       <width>211</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:14pt;&quot;&gt;
      Введите номер карты:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="label_4">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>480</y>
       <width>211</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:14pt;&quot;&gt;
      Введите CVV карты:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QPushButton" name="finish_reg">
     <property name="geometry">
      <rect>
       <x>390</x>
       <y>620</y>
       <width>191</width>
       <height>91</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>Завершить регестрацию</string>
     </property>
    </widget>
    <widget class="QLabel" name="name_error">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>130</y>
       <width>281</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">color: rgb(170, 0, 0);
font: 10pt &quot;MS Shell Dlg 2&quot;;</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/&gt;
      &lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLineEdit" name="register_name">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>80</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLineEdit" name="register_password">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>220</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLineEdit" name="register_card_number">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>360</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLineEdit" name="register_cvv_card">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>500</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLabel" name="password_error">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>270</y>
       <width>281</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 10pt &quot;MS Shell Dlg 2&quot;;
color: rgb(170, 0, 0);</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/&gt;
      &lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="card_error">
     <property name="geometry">
      <rect>
       <x>230</x>
       <y>410</y>
       <width>421</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 10pt &quot;MS Shell Dlg 2&quot;;
color: rgb(170, 0, 0);</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/&gt;
      &lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="cvv_error">
     <property name="geometry">
      <rect>
       <x>300</x>
       <y>550</y>
       <width>281</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 10pt &quot;MS Shell Dlg 2&quot;;
color: rgb(170, 0, 0);</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/&gt;
      &lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="pict2">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>651</width>
       <height>761</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QPushButton" name="cancell_button">
     <property name="geometry">
      <rect>
       <x>60</x>
       <y>620</y>
       <width>191</width>
       <height>91</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(170, 0, 0);
</string>
     </property>
     <property name="text">
      <string>Отмена</string>
     </property>
    </widget>
    <zorder>pict2</zorder>
    <zorder>label_4</zorder>
    <zorder>label</zorder>
    <zorder>label_2</zorder>
    <zorder>label_3</zorder>
    <zorder>finish_reg</zorder>
    <zorder>name_error</zorder>
    <zorder>register_name</zorder>
    <zorder>register_password</zorder>
    <zorder>register_card_number</zorder>
    <zorder>register_cvv_card</zorder>
    <zorder>password_error</zorder>
    <zorder>card_error</zorder>
    <zorder>cvv_error</zorder>
    <zorder>cancell_button</zorder>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>"""

casino_project3 = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>651</width>
    <height>761</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="enter_layout" native="true">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>661</width>
      <height>761</height>
     </rect>
    </property>
    <property name="acceptDrops">
     <bool>false</bool>
    </property>
    <widget class="QLabel" name="label">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>220</y>
       <width>201</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:16pt;&quot;&gt;
      Введите логин:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="label_2">
     <property name="geometry">
      <rect>
       <x>50</x>
       <y>380</y>
       <width>211</width>
       <height>61</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:16pt;&quot;&gt;
      Введите пароль:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QPushButton" name="finish_ent">
     <property name="geometry">
      <rect>
       <x>400</x>
       <y>590</y>
       <width>191</width>
       <height>91</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(0, 0, 127);
</string>
     </property>
     <property name="text">
      <string>Войти</string>
     </property>
    </widget>
    <widget class="QLabel" name="name_error">
     <property name="geometry">
      <rect>
       <x>310</x>
       <y>290</y>
       <width>281</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">color: rgb(170, 0, 0);
font: 10pt &quot;MS Shell Dlg 2&quot;;</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/
      &gt;&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLineEdit" name="enter_name">
     <property name="geometry">
      <rect>
       <x>270</x>
       <y>240</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLineEdit" name="enter_password">
     <property name="geometry">
      <rect>
       <x>270</x>
       <y>400</y>
       <width>281</width>
       <height>31</height>
      </rect>
     </property>
    </widget>
    <widget class="QLabel" name="password_error">
     <property name="geometry">
      <rect>
       <x>310</x>
       <y>450</y>
       <width>281</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">color: rgb(170, 0, 0);
font: 10pt &quot;MS Shell Dlg 2&quot;;</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:10pt;&quot;&gt;&lt;br/&gt;
      &lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="pict3">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>651</width>
       <height>761</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QPushButton" name="cancell_button">
     <property name="geometry">
      <rect>
       <x>60</x>
       <y>590</y>
       <width>191</width>
       <height>91</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">
color: rgb(170, 0, 0);
</string>
     </property>
     <property name="text">
      <string>Отмена</string>
     </property>
    </widget>
    <zorder>pict3</zorder>
    <zorder>label</zorder>
    <zorder>label_2</zorder>
    <zorder>finish_ent</zorder>
    <zorder>name_error</zorder>
    <zorder>enter_name</zorder>
    <zorder>enter_password</zorder>
    <zorder>password_error</zorder>
    <zorder>cancell_button</zorder>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>651</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

casino_project4 = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>651</width>
    <height>781</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="main_layout" native="true">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>651</width>
      <height>761</height>
     </rect>
    </property>
    <widget class="QPushButton" name="replenish_button">
     <property name="geometry">
      <rect>
       <x>480</x>
       <y>40</y>
       <width>75</width>
       <height>23</height>
      </rect>
     </property>
     <property name="text">
      <string>пополнить</string>
     </property>
    </widget>
    <widget class="QPushButton" name="withdraw_button">
     <property name="geometry">
      <rect>
       <x>570</x>
       <y>40</y>
       <width>75</width>
       <height>23</height>
      </rect>
     </property>
     <property name="text">
      <string>снять</string>
     </property>
    </widget>
    <widget class="QLabel" name="pict4">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>651</width>
       <height>761</height>
      </rect>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;br/&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="table_result">
     <property name="geometry">
      <rect>
       <x>10</x>
       <y>10</y>
       <width>191</width>
       <height>271</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QPushButton" name="spin_button">
     <property name="geometry">
      <rect>
       <x>520</x>
       <y>360</y>
       <width>71</width>
       <height>71</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">background-color: rgb(255, 255, 127);</string>
     </property>
     <property name="text">
      <string>Spin</string>
     </property>
    </widget>
    <widget class="QLabel" name="balance_label">
     <property name="geometry">
      <rect>
       <x>490</x>
       <y>70</y>
       <width>151</width>
       <height>31</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 75 9pt &quot;MS Shell Dlg 2&quot;;</string>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QPushButton" name="exit_button">
     <property name="geometry">
      <rect>
       <x>20</x>
       <y>700</y>
       <width>81</width>
       <height>31</height>
      </rect>
     </property>
     <property name="text">
      <string>Выйти</string>
     </property>
    </widget>
    <widget class="QLabel" name="login_label">
     <property name="geometry">
      <rect>
       <x>490</x>
       <y>10</y>
       <width>151</width>
       <height>31</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 12pt &quot;MS Shell Dlg 2&quot;;
color: rgb(0, 0, 127);</string>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QComboBox" name="bet_combobox">
     <property name="geometry">
      <rect>
       <x>520</x>
       <y>320</y>
       <width>69</width>
       <height>22</height>
      </rect>
     </property>
     <item>
      <property name="text">
       <string>50</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>100</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>200</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>500</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>1000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>2000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>5000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>10000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>25000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>50000</string>
      </property>
     </item>
     <item>
      <property name="text">
       <string>100000</string>
      </property>
     </item>
    </widget>
    <widget class="QLabel" name="troll_label">
     <property name="geometry">
      <rect>
       <x>170</x>
       <y>510</y>
       <width>251</width>
       <height>41</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 10pt &quot;MS Shell Dlg 2&quot;;
background-color: rgb(232, 209, 209);
border-radius: 10px;</string>
     </property>
     <property name="text">
      <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p align=&quot;center&quot;&gt;TextLabel&lt;/p&gt;&lt;/body&gt;
      &lt;/html&gt;</string>
     </property>
    </widget>
    <widget class="QLabel" name="spin_error">
     <property name="geometry">
      <rect>
       <x>510</x>
       <y>460</y>
       <width>121</width>
       <height>21</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true"/>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QLabel" name="info_label">
     <property name="geometry">
      <rect>
       <x>170</x>
       <y>450</y>
       <width>251</width>
       <height>41</height>
      </rect>
     </property>
     <property name="styleSheet">
      <string notr="true">font: 12pt &quot;MS Shell Dlg 2&quot;;
color: rgb(0, 0, 127);</string>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QLabel" name="slot1">
     <property name="geometry">
      <rect>
       <x>160</x>
       <y>320</y>
       <width>109</width>
       <height>109</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QLabel" name="slot2">
     <property name="geometry">
      <rect>
       <x>270</x>
       <y>320</y>
       <width>109</width>
       <height>109</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QLabel" name="slot3">
     <property name="geometry">
      <rect>
       <x>380</x>
       <y>320</y>
       <width>109</width>
       <height>109</height>
      </rect>
     </property>
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
    <widget class="QLabel" name="label">
     <property name="geometry">
      <rect>
       <x>520</x>
       <y>290</y>
       <width>71</width>
       <height>21</height>
      </rect>
     </property>
     <property name="text">
      <string>Ваша ставка</string>
     </property>
    </widget>
    <zorder>pict4</zorder>
    <zorder>replenish_button</zorder>
    <zorder>withdraw_button</zorder>
    <zorder>table_result</zorder>
    <zorder>spin_button</zorder>
    <zorder>balance_label</zorder>
    <zorder>exit_button</zorder>
    <zorder>login_label</zorder>
    <zorder>bet_combobox</zorder>
    <zorder>troll_label</zorder>
    <zorder>spin_error</zorder>
    <zorder>info_label</zorder>
    <zorder>slot1</zorder>
    <zorder>slot2</zorder>
    <zorder>slot3</zorder>
    <zorder>label</zorder>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Start_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        cp = io.StringIO(casino_project)
        uic.loadUi(cp, self)
        self.setFixedSize(651, 761)
        self.pict1.setPixmap(QPixmap('online-casino-slots.png'))
        self.register_button.clicked.connect(self.register_window)
        self.enter_button.clicked.connect(self.enter_window)

    def register_window(self):
        self.rw = Register_Window()
        self.setCentralWidget(self.rw)
        self.rw.show()
        self.sw = Start_Window()
        self.sw.setVisible(False)

    def enter_window(self):
        self.ew = Enter_Window()
        self.setCentralWidget(self.ew)
        self.ew.show()
        self.sw = Start_Window()
        self.sw.setVisible(False)


class Register_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        cp2 = io.StringIO(casino_project2)
        uic.loadUi(cp2, self)
        self.setFixedSize(651, 761)
        self.pict2.setPixmap(QPixmap('Casino_background.png'))
        self.finish_reg.clicked.connect(self.register_finish)
        self.cancell_button.clicked.connect(self.cancell)

    def cancell(self):
        self.sw = Start_Window()
        self.setCentralWidget(self.sw)
        self.sw.show()
        self.rw = Register_Window()
        self.rw.setVisible(False)

    def register_finish(self):
        self.flag = True

        self.login = self.register_name.text()
        self.login_error = False
        self.password = self.register_password.text()
        self.card = self.register_card_number.text()
        self.card_check = True
        self.card_check2 = True
        self.cvv = self.register_cvv_card.text()
        self.cvv_check = True
        self.cvv_check2 = True

        self.name_error.setText('')
        self.password_error.setText('')
        self.card_error.setText('')
        self.cvv_error.setText('')

        #  Ошибка логина
        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        for i in cur.execute("SELECT login from client_data").fetchall():
            if self.login in i:
                self.login_error = True
                break
        if len(self.login) <= 3:
            self.name_error.setText('Логин должен содержать 4 или более символа')
            self.flag = False
        elif ' ' in self.login:
            self.name_error.setText('Логин не должен содержать пробелы')
            self.flag = False
        elif self.login_error:
            self.name_error.setText('Данный логин уже существует')
            self.flag = False
        f.close()

        #  Ошибка пароля
        if len(self.password) < 4:
            self.password_error.setText('Пароль слишком маленький')
            self.flag = False
        elif ' ' in self.password:
            self.password_error.setText('Пароль не должен содержать пробелы')
            self.flag = False

        #  Ошибка карты - не 19 символов
        if len(self.card) != 19:
            self.flag = False
            self.card_error.setText('Номер карты должен содержать 19 символов включая пробелы')

        # Ошибка карты - неправильный порядок символов
        for i in range(len(self.card)):
            if self.card[i] != ' ' and (i + 1) % 5 == 0:
                self.flag = False
                self.card_check = False
                break
            if self.card[i] not in NUMBER and (i + 1) % 5 != 0:
                self.flag = False
                self.card_check = False
                break
        if self.card_check is False and self.card_check2:
            self.card_error.setText('Номер карты должен содержать только цифры и пробелы в нужных местах')

        #  ошибка cvv - не 3 символа
        if len(self.cvv) != 3:
            self.cvv_check2 = False
            self.flag = False
            self.cvv_error.setText('CVV карты должен сожержать ровно 3 цифры')
        #  онибка cvv - присутствие не цифр
        for i in self.cvv:
            if i not in NUMBER:
                self.flag = False
                self.cvv_check = False
        if self.cvv_check is False and self.cvv_check2:
            self.cvv_error.setText('CVV карты должен содержать только цифры')
        if self.flag:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            cur.execute(f"""INSERT INTO client_data(login,password,balance) VALUES('{self.login}', '{self.password}', 
            {0})""")
            f.commit()
            f.close()
            self.mw = Main_Window(self, self.login, 0)
            self.setCentralWidget(self.mw)
            self.mw.show()
            self.rw = Register_Window()
            self.rw.setVisible(False)


class Enter_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        cp3 = io.StringIO(casino_project3)
        uic.loadUi(cp3, self)
        self.setFixedSize(651, 761)
        self.pict3.setPixmap(QPixmap('Casino_background.png'))

        self.finish_ent.clicked.connect(self.enter_finish)
        self.cancell_button.clicked.connect(self.cancell)

    def cancell(self):
        self.sw = Start_Window()
        self.setCentralWidget(self.sw)
        self.sw.show()
        self.ew = Enter_Window()
        self.ew.setVisible(False)

    def enter_finish(self):
        self.flag = True
        self.login_check = True

        self.login = self.enter_name.text()
        self.password = self.enter_password.text()

        self.name_error.setText('')
        self.password_error.setText('')

        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        # ошибка логина
        for i in cur.execute("SELECT login from client_data").fetchall():
            if self.login in i:
                self.login_check = False
                break
        if self.login_check:
            self.flag = False
            self.name_error.setText('Такого логина не существует')
        # ошибка пароля
        elif self.password != ''.join(cur.execute(f"""SELECT password from client_data 
        WHERE login = '{self.login}'""").fetchone()):
            self.flag = False
            self.password_error.setText('Неверный пароль')
        f.close()
        if self.flag:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            balance = cur.execute(f"""SELECT balance from client_data 
                    WHERE login = '{self.login}'""").fetchone()
            self.mw = Main_Window(self, self.login, int(*balance))
            self.setCentralWidget(self.mw)
            self.mw.show()
            self.ew = Enter_Window()
            self.ew.setVisible(False)


class Main_Window(QMainWindow):
    def __init__(self, *arg):
        super().__init__()
        self.login = arg[1]
        self.balance = arg[2]  # должно быть всегда int
        cp4 = io.StringIO(casino_project4)
        uic.loadUi(cp4, self)
        self.setFixedSize(651, 761)
        self.pict4.setPixmap(QPixmap('Casino_patern.png'))
        self.table_result.setPixmap(QPixmap('Slot_value_table.png'))

        self.login_label.setText(self.login)
        self.balance_label.setText(f'Ваш баланс: {self.balance}')
        self.spin_error.setText('')
        self.troll_label.setText('')
        self.info_label.setText('')
        self.slot1.setPixmap(QPixmap(SLOT_PICTURE['.']))
        self.slot2.setPixmap(QPixmap(SLOT_PICTURE['.']))
        self.slot3.setPixmap(QPixmap(SLOT_PICTURE['.']))

        self.replenish_button.clicked.connect(self.replenish_method)  # Пополнить
        self.withdraw_button.clicked.connect(self.withdraw_method)  # Снять
        self.spin_button.clicked.connect(self.spin)  # spin
        self.exit_button.clicked.connect(self.exit)  # выйти

    def replenish_method(self):
        value, ok_pressed = QInputDialog.getInt(self, 'Пополнение',
                                                'Введите пополняемую сумму', 100, 100, 1000000, 100)
        if ok_pressed:
            f = sqlite3.connect('Casino_database.db')
            cur = f.cursor()
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(value)} WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
            where login = '{self.login}'""").fetchone())
            f.close()
            file = open('receipts.txt', mode='a')
            file.write(f'Пользователь {self.login} пополнил {str(value)}. '
                       f'Текущий баланс пользователя {self.balance}.\n')
            file.close()
            self.balance_label.setText(f'Ваш баланс: {self.balance}')

    def withdraw_method(self):
        f = sqlite3.connect('Casino_database.db')
        cur = f.cursor()
        value, ok_pressed = QInputDialog.getInt(self, 'Снятие', 'Введите снимаемую сумму', 0, 0,
                                                int(*cur.execute(f"""SELECT balance from client_data WHERE login = 
                                                '{self.login}'""").fetchone()), 100)
        if ok_pressed:
            cur.execute(f"""UPDATE client_data SET balance = balance - {str(value)} WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                        where login = '{self.login}'""").fetchone())
            if int(value) != 0:
                file = open('receipts.txt', mode='a')
                file.write(f'Пользователь {self.login} снял {str(value)}. '
                           f'Текущий баланс пользователя {self.balance}.\n')
                file.close()
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
        f.close()

    def exit(self):
        self.sw = Start_Window()
        self.setCentralWidget(self.sw)
        self.sw.show()
        self.mw = Main_Window(self, None, None)
        self.mw.setVisible(False)

    def spin(self):
        f = sqlite3.connect('Casino_database.db')
        self.spin_error.setText('')
        cur = f.cursor()
        sl1 = choice(SLOTS_TYPES)
        sl2 = choice(SLOTS_TYPES)
        sl3 = choice(SLOTS_TYPES)
        bet = int(self.bet_combobox.currentText())
        # ошибка в случае если ставка превышает баланс
        if bet > self.balance:
            self.spin_error.setText('Не хватает средств')
            self.troll_label.setText('')
            self.info_label.setText('')
            self.slot1.setPixmap(QPixmap(SLOT_PICTURE['.']))
            self.slot2.setPixmap(QPixmap(SLOT_PICTURE['.']))
            self.slot3.setPixmap(QPixmap(SLOT_PICTURE['.']))
            return None
        cherry_count = 0
        for i in (sl1, sl2, sl3):
            if i == 'c':
                cherry_count += 1

        # 7 wins
        if sl1 == sl2 == sl3 == '7':
            result = bet * 1000
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # bar wins
        elif sl1 == sl2 == sl3 == 'bar':
            result = bet * 300
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # bell wins
        elif sl1 == sl2 == sl3 == 'b':
            result = bet * 80
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # grape wins
        elif sl1 == sl2 == sl3 == 'g':
            result = bet * 50
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # lemon wins
        elif sl1 == sl2 == sl3 == 'l':
            result = bet * 25
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry3 wins
        elif cherry_count == 3:
            result = bet * 100
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry2 wins
        elif cherry_count == 2:
            result = bet * 10
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        # cherry1 wins
        elif cherry_count == 1:
            result = bet * 2
            cur.execute(f"""UPDATE client_data SET balance = balance + {str(result)} - {str(bet)} 
            WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                    where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(VICTORY_PHRASES))
            self.info_label.setText(f'Вы выйграли: {result}')
        else:
            cur.execute(f"""UPDATE client_data SET balance = balance - {str(bet)} 
                        WHERE login = '{self.login}'""")
            f.commit()
            self.balance = int(*cur.execute(f"""SELECT balance from client_data 
                                                where login = '{self.login}'""").fetchone())
            self.balance_label.setText(f'Ваш баланс: {self.balance}')
            self.troll_label.setText(choice(TROLL_PHRASES))
            self.info_label.setText(f'Вы проиграли')
        self.slot1.setPixmap(QPixmap(SLOT_PICTURE[sl1]))
        self.slot2.setPixmap(QPixmap(SLOT_PICTURE[sl2]))
        self.slot3.setPixmap(QPixmap(SLOT_PICTURE[sl3]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Window()
    ex.show()
    sys.exit(app.exec())

