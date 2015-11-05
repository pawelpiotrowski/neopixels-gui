#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

""" Neopixel GUI App """

import tkinter as AppTK
from tkinter import ttk as AppTTK
import serial as AppSerial

import serialports as serial_ports
import neoapi

__author__ = 'pawelpiotrowski'

APP_PADDING = '15 15 15 15'
APP_TITLE = 'Neopixel GUI'
APP_BAUDRATE = 9600
SERIAL_MONITOR = False

class Application(AppTK.Tk):
	def __init__(self, parent):
		AppTK.Tk.__init__(self, parent)
		self.parent = parent
		self.pixel_command_val = AppTK.StringVar()
		self.pixels_ctrl_widget = AppTTK.Frame(self.parent, padding=APP_PADDING)
		self.ports_widget = AppTTK.Frame(self.parent, padding=APP_PADDING)
		self.ports = serial_ports.get_ports()
		self.port = AppTK.StringVar()
		self.port_status = AppTK.StringVar()
		self.ports_button = AppTTK.Button(self.ports_widget)
		self.serial = AppSerial.Serial()
		self.serial.baudrate = APP_BAUDRATE
		self.serial.timeout = 1
		self.start()

	def start(self):
		self.grid()
		self.grid_columnconfigure(0, weight=1)
		self.display_ports_widget()
		self.display_pixels_ctrl_widget()

	def display_ports_widget(self):
		self.ports_widget.grid(column=0, row=0, sticky='W, E')

		self.port_status.set('Choose port to connect:')
		port_status = AppTTK.Label(self.ports_widget, textvariable=self.port_status)
		port_status.grid(column=0, padx=2, row=0, sticky='W')

		ports_combo = AppTTK.Combobox(self.ports_widget, state='readonly', width=30)
		ports_combo['textvariable'] = self.port
		ports_combo['values'] = (', '.join(self.ports))
		ports_combo.grid(column=0, row=1)
		ports_combo.bind('<<ComboboxSelected>>', self.display_port_connect)

		self.ports_button['text'] = 'Connect'
		self.ports_button['command'] = self.port_connect
		self.ports_button['state'] = 'disabled'
		self.ports_button.grid(column=1, row=1)

	def display_pixels_ctrl_widget(self):
		self.pixels_ctrl_widget.grid(column=0, row=1, sticky='W, E')
		pixel_command = AppTTK.Entry(self.pixels_ctrl_widget, textvariable=self.pixel_command_val)
		pixel_command.grid(column=0, row=0)
		pixel_command.bind('<Return>', self.send_pixels_command)
		pixel_command_button = AppTTK.Button(self.pixels_ctrl_widget)
		pixel_command_button['text'] = 'Send'
		pixel_command_button['command'] = self.send_pixels_command
		pixel_command_button.grid(column=1, row=0)

	def send_pixels_command(self, *ev):
		command = self.pixel_command_val.get().strip()
		self.pixel_command_val.set('')
		if len(command):
			command = neoapi.validate_command(command)
			print([command])
			self.serial.write(bytes(command, 'ASCII'))

	def display_port_connect(self, *ev):
		self.port_status.set('Press connect')
		self.ports_button['state'] = 'normal'

	def port_connect(self):
		print('inside port_connect')
		""" ser.write(bytes('200\n','ASCII')) """

		if self.serial.isOpen():
			print('port close')
			self.port_status.set('Disconnecting...')
			self.serial.close()
			self.port_status.set('Press connect')
			self.ports_button['text'] = 'Connect'
		else:
			print('port open')
			port = self.port.get()
			if SERIAL_MONITOR:
				port = port.replace('/tty.', '/cu.')
			self.port_status.set('Connecting...')
			self.serial.port = port
			print(self.serial.port)
			self.serial.open()
			self.port_status.set('Connected')
			self.ports_button['text'] = 'Disconnect'


app = Application(None)
app.title(APP_TITLE)
app.mainloop()
