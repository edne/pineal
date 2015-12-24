#include <SFML/Graphics.hpp>

class Entity;
class Drawable;
class Shape;
class Surface;


class Entity {};

class Drawable : public Entity {
    public:
        virtual ~Drawable();
        virtual void draw(sf::RenderTarget*);
};

class Shape : public Drawable {
    public:
        virtual ~Shape();
        void fill(double r, double g, double b, double a);
        void stroke(double r, double g, double b, double a);
        void line(double t);
        virtual void draw(sf::RenderTarget* target);

    protected:
        sf::Color sf_fill, sf_stroke;
        double thickness;
};

class Surface : public Entity {
    public:
        virtual ~Surface();
        virtual void render(Drawable* child);
};

class Polygon : public Shape {
    public:
        Polygon(int);
        static Polygon* memo(int n);
        void draw(sf::RenderTarget*);

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
