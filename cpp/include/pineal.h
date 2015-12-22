#include <SFML/Graphics.hpp>

class Polygon;
class Window;

class Window {
    public:
        Window(const char*);
        void display(Polygon*);
        bool is_open();
        static Window* memo(const char*);
        sf::RenderTarget* get_target() {return &sf_window;};

    private:
        sf::RenderWindow sf_window;
};

class Polygon {
    public:
        Polygon(int);
        void draw(Window*);
        static Polygon* memo(int);

   private:
        sf::CircleShape sf_polygon;
};
