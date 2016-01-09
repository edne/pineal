#include <SFML/Graphics.hpp>

class Entity;
class Drawable;
class Shape;
class Surface;


class Signal {
    public:
        Signal(double x, double y, double z, double w)
            : xs{x, y, z, w} {};

        Signal(double x, double y, double z)
            : xs{x, y, z, 0} {};

        Signal(double x, double y)
            : xs{x, y, 0, 0} {};

        Signal(double x)
            : xs{x, 0, 0, 0} {};

        Signal()
            : xs{0, 0, 0, 0} {};

        double x() { return xs[0]; }
        double y() { return xs[1]; }
        double z() { return xs[2]; }
        double w() { return xs[3]; }

    private:
        double xs[4];
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

class Entity {
    public:
        virtual void attribute(std::string key, Color c) {};
        virtual void attribute(std::string key, double x) {};
        virtual void attribute(std::string key, double x, double y) {};

        virtual ~Entity() {};
};

class Drawable : public Entity {
    public:
        virtual void draw(sf::RenderTarget* target) {};
        virtual ~Drawable() {};
};

class Surface : public Entity {
    public:
        virtual void render(Drawable* child) {};
        virtual ~Surface() {};
};

class Group : public Drawable {
    public:
        Group() {};

        virtual void attribute(std::string key, Color c);
        virtual void attribute(std::string key, double x);
        virtual void attribute(std::string key, double x, double y);

        void add(Drawable* d);
        void draw(sf::RenderTarget* target);

    private:
        std::vector<Drawable*> elements;
};

class Polygon : public Drawable {
    public:
        Polygon(int);

        void attribute(std::string key, Color c);
        void attribute(std::string key, double x);
        void attribute(std::string key, double x, double y);

        void draw(sf::RenderTarget* target);

    protected:
        sf::CircleShape sf_shape;
};

class Window : public Surface {
    public:
        Window(const char* name);
        void render(Drawable* child);
        bool is_open();
        static Window* memo(const char* name);

    private:
        sf::RenderWindow sf_window;
};
