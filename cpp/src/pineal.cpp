#include <memory>
#include <SFML/Graphics.hpp>
#include <pineal.h>

using namespace std;


template<class T, typename K>
T* memorize(K name) {
    // I can not use templates in SWIG interfaces
    static map<K, unique_ptr<T>> memory;

    if (memory.count(name) == 0) {
        memory[name] = unique_ptr<T>(new T(name));
    }
    return memory[name].get();
}


Window::Window(const char* name) {
    sf_window.create(sf::VideoMode(800, 600), name);
}

bool Window::is_open() {
    return sf_window.isOpen();
}

void Window::display(Polygon* child) {
    sf::Event event;

    while (sf_window.pollEvent(event)) {
        if (event.type == sf::Event::Closed)
            sf_window.close();
    }

    sf_window.clear(sf::Color::Black);

    child->draw(this);

    sf_window.display();
}

Window* Window::memo(const char* name) {
    return memorize<Window>(name);
}


Polygon::Polygon(int n) {
    sf_polygon = sf::CircleShape(100);
    sf_polygon.setPointCount(n);
}

void Polygon::draw(Window* surface) {
    surface->get_target()->draw(sf_polygon);
}

Polygon* Polygon::memo(int n) {
    return memorize<Polygon>(n);
}
