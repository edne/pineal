#include <SFML/Graphics.hpp>

class Entity {
    public:
        void draw() {};
};


class Window {
    public:
        Window(const char*);
        bool is_open();
        void draw();

    private:
        sf::RenderWindow sf_window;
};

void window(const char*);
