#include <SFML/Graphics.hpp>

class Polygon;
class Window;

class Window {
    public:
        Window(const char*);
        void display(Polygon*);
        bool is_open();
        static Window* memo(const char*);

    private:
        sf::RenderWindow sf_window;
};

class Polygon {
    public:
        Polygon(int);
        sf::CircleShape draw();
        static Polygon* memo(int);

   private:
        sf::CircleShape sf_polygon;
};
