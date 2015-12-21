#include <SFML/Graphics.hpp>
#include <pineal.h>


Window :: Window(const char* name) {
    sf_window.create(sf::VideoMode(800, 600), name);
}

bool Window :: is_open() {
    return sf_window.isOpen();
}

void Window :: draw() {
    sf::Event event;

    while (sf_window.pollEvent(event)) {
        if (event.type == sf::Event::Closed)
            sf_window.close();
    }

    sf_window.clear(sf::Color::Black);

    // draw everything here...
    // window.draw(...);

    sf_window.display();
}

Window*  Window :: memo(const char* name) {
    static std::map <const char*, Window*> memory;
    Window *w;

    if (memory.count(name) == 0) {
        w = new Window(name);
        memory[name] = w;
    }
    else
        w = memory[name];

    return w;
}

