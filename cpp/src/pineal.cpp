#include <SFML/Graphics.hpp>
#include <pineal.h>

template<class T, typename K>
T* memorize(K name) {
    // I can not use templates in SWIG interfaces
    static std::map <K, T*> memory;
    T *e;

    if (memory.count(name) == 0) {
        e = new T(name);
        memory[name] = e;
    }
    else
        e = memory[name];

    return e;
}


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

Window* Window :: memo(const char* name) {
    return memorize<Window>(name);
}

