#include <SFML/Graphics.hpp>

class Entity;
class Drawable;
class Shape;
class Surface;


class Color {
    public:
        Color(double r, double g, double b, double a)
            : r(r), g(g), b(b), a(a) {};

        Color(double r, double g, double b)
            : Color(r, g, b, 1) {};

        Color(double x, double a)
            : Color(x, x, x, a) {};

        Color(double x): Color(x, x, x, 1) {};

        double r, g, b, a;
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
