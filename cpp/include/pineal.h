#include <SFML/Graphics.hpp>

class Entity {
    public:
        void draw() {};
};


class Window : Entity {
    public:
        void draw();
        bool is_open();
        static Window* memo(const char*);

    private:
        Window(const char*);
        sf::RenderWindow sf_window;
};
