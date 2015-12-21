#include <SFML/Graphics.hpp>

class Entity {
    public:
        void draw() {};
};


class Window : Entity {
    public:
        Window(const char*);
        void draw();
        bool is_open();
        static Window* memo(const char*);

    private:
        sf::RenderWindow sf_window;
};
