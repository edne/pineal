class Signal {
    public:
        Signal(double x, double y, double z, double w)
            : xs{x, y, z, w}, n_(4) {};

        Signal(double x, double y, double z)
            : xs{x, y, z, 0}, n_(3) {};

        Signal(double x, double y)
            : xs{x, y, 0, 0}, n_(2) {};

        Signal(double x)
            : xs{x, 0, 0, 0}, n_(1) {};

        Signal()
            : xs{0, 0, 0, 0} , n_(0){};

        Signal(Signal* s)
        : xs{s->x(), s->y(), s->z(), s->w()}, n_(s->n()) {};

        Signal(std::string name) : Signal() {};

        static Signal* memo(std::string name);

        void set_x(double x) { xs[0] = x; }
        void set_y(double y) { xs[1] = y; }
        void set_z(double z) { xs[2] = z; }
        void set_w(double w) { xs[3] = w; }

        double x() { return xs[0]; }
        double y() { return xs[1]; }
        double z() { return xs[2]; }
        double w() { return xs[3]; }

        int n() { return n_; }

    private:
        double xs[4];
        int n_;
};

class Color : public Signal {
    public:
        Color(double r, double g, double b, double a)
            : Signal(r, g, b, a) {};

        Color(double r, double g, double b)
            : Signal(r, g, b, 1) {};

        Color(double x, double a)
            : Signal(x, x, x, a) {};

        Color(double x)
            : Signal(x, x, x, 1) {};

        double r() { return x(); }
        double g() { return y(); }
        double b() { return z(); }
        double a() { return w(); }
};
