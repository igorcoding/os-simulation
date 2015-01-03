import os
from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf
import math
from src.simulation import Simulation
from threading import Thread, Event


GLADE_MARKUP = 'os-simulator.glade'


class Dialog(Gtk.Dialog):
    def __init__(self, parent, title, message):
        Gtk.Dialog.__init__(self, title, parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        # self.set_default_size(150, 100)

        label = Gtk.Label(message)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class OsSimulatorWindow(object):
    AVG_INNER_PLOT = 'avg_inner.png'
    AVG_TOTAL_PLOT = 'avg_total.png'

    def __init__(self, builder):
        super(OsSimulatorWindow, self).__init__()
        self.builder = builder
        self.builder.connect_signals(self)
        self.window = builder.get_object('os_simulator_window')
        self.delta_text = builder.get_object('delta_text')
        self.buffer_size_text = builder.get_object('buffer_size_text')
        self.buffer_latency_text = {
            'min': builder.get_object('buffer_latency_min_text'),
            'max': builder.get_object('buffer_latency_max_text'),
            'step': builder.get_object('buffer_latency_step_text'),
        }
        self.gen_lambda_text = {
            'min': builder.get_object('lambda_min_text'),
            'max': builder.get_object('lambda_max_text'),
            'step': builder.get_object('lambda_step_text'),
        }
        self.time_distrib_text = {
            'mu': builder.get_object('solve_time_distrib_mu_text'),
            'sigma': builder.get_object('solve_time_distrib_sigma_text'),
        }
        self.simulation_time_text = builder.get_object('simulation_time_text')
        self.exp_per_conf_text = builder.get_object('exp_per_conf_text')
        self.sim_finished_event = Event()

        self.images_box = builder.get_object('images_box')
        self.images = {
            'inner': builder.get_object('avg_inner_plot'),
            'total': builder.get_object('avg_total_plot'),
        }

        self.simulation_thread = None
        self.simulation_finished = False

    def show(self):
        self.window.show_all()

    def on_os_simulator_window_configure_event(self, *args):
        if self.simulation_finished:
            self._draw_images()

    def on_os_simulator_window_destroy(self, *args):
        if self.simulation_thread is not None:
            # self.simulation_thread.stop()
            pass
        Gtk.main_quit(*args)

    def on_simulate_button_clicked(self, *args):
        try:
            delta = int(self.delta_text.get_text())
            buffer_size = int(self.buffer_size_text.get_text())
            buffer_latency = xrange(int(self.buffer_latency_text['min'].get_text()),
                                    int(self.buffer_latency_text['max'].get_text()),
                                    int(self.buffer_latency_text['step'].get_text()))
            gen_lambda = xrange(int(self.gen_lambda_text['min'].get_text()),
                                int(self.gen_lambda_text['max'].get_text()),
                                int(self.gen_lambda_text['step'].get_text()))

            time_distrib = dict(mu=float(self.time_distrib_text['mu'].get_text()),
                                sigma=float(self.time_distrib_text['sigma'].get_text()))

            sim_time = int(self.simulation_time_text.get_text())
            exp_per_conf = int(self.exp_per_conf_text.get_text())
            data = dict(delta=delta, buffer_size=buffer_size, buffer_latency=buffer_latency,
                        gen_lambda=gen_lambda, time_distrib=time_distrib, sim_time=sim_time,
                        exp_per_conf=exp_per_conf)

            def target():
                self.on_simulation_started()
                Simulation().simulation(**data)
                GLib.idle_add(self.on_simulation_finished)

            self.simulation_thread = Thread(target=target)
            self.simulation_thread.start()

        except ValueError as e:
            self.display_dialog('Error', 'Incorrect data')
            print e
        pass

    def display_dialog(self, title, message):
        dialog = Dialog(self.window, title, message)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")

        dialog.destroy()

    def on_simulation_started(self):
        print 'Simulation started'
        self.simulation_finished = False
        if os.path.isfile(self.AVG_INNER_PLOT):
            os.remove(self.AVG_INNER_PLOT)
        if os.path.isfile(self.AVG_TOTAL_PLOT):
            os.remove(self.AVG_TOTAL_PLOT)

    def on_simulation_finished(self):
        print 'Simulation finished'
        self.simulation_finished = True
        self.display_dialog("Info", "finished")

        self._draw_images()

    def _draw_images(self):
        rect = self.images_box.get_allocation()
        width = rect.width
        height = rect.height / 2

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.AVG_INNER_PLOT)
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self.images['inner'].set_from_pixbuf(pixbuf)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.AVG_TOTAL_PLOT)
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self.images['total'].set_from_pixbuf(pixbuf)

    @staticmethod
    def _float_range(first, last, step):
        eps = 0.00001
        l = []
        current = first
        while math.fabs(current - last) >= eps:
            l.append(current)
            current += step
        return l


if __name__ == "__main__":
    GObject.threads_init()
    builder = Gtk.Builder()
    builder.add_from_file(GLADE_MARKUP)
    window = OsSimulatorWindow(builder)
    window.show()
    Gtk.main()
