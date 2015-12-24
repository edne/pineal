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
        //virtual Shape* fill(double r, double g, double b, double a) = 0;
};

class Surface : public Entity {
    public:
        virtual ~Surface();
        virtual void render(Drawable* child);
};

class Polygon : public Shape {
    public:
        Polygon(int);
        void draw(sf::RenderTarget*);
        Shape* fill(double r, double g, double b, double a);

    protected:
        sf::CircleShape sf_shape;  // TODO use sf::Shape in Shape
        sf::Color sf_fill;
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
