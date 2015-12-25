#include <SFML/Graphics.hpp>

class Entity;
class Drawable;
class Shape;
class Surface;


class Entity {};

class Color {
    public:
        Color(double r, double g, double b, double a);
        Color(double r, double g, double b);
        Color(double x, double a);
        Color(double x);

        double r, g, b, a;
};

class Drawable : public Entity {
    public:
        virtual ~Drawable();
        virtual void draw(sf::RenderTarget*);
};

class Shape : public Drawable {
    public:
        void fill(Color c);
        void stroke(Color c);
        void line(double t);

        virtual void draw(sf::RenderTarget* target);
        virtual ~Shape();

    protected:
        sf::Color sf_fill, sf_stroke;
        double thickness;
};

class Surface : public Entity {
    public:
        virtual void render(Drawable* child);
        virtual ~Surface();
};

class Polygon : public Shape {
    public:
        Polygon(int);
        void draw(sf::RenderTarget*);
        //static Polygon* memo(int n);

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
