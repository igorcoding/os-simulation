from gi.repository import Gtk, GLib, GObject
from src.simulation import simulation
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

    def show(self):
        self.window.show_all()

    @staticmethod
    def on_os_simulator_window_destroy(*args):
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
                simulation(**data)
                GLib.idle_add(self.display_dialog, "Info", "finished")

            th = Thread(target=target)
            th.start()

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


if __name__ == "__main__":
    GObject.threads_init()
    builder = Gtk.Builder()
    builder.add_from_file(GLADE_MARKUP)
    window = OsSimulatorWindow(builder)
    window.show()
    Gtk.main()
