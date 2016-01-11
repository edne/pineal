#include <SFML/Graphics.hpp>
#include <pineal.hpp>
#include <memory>
#include <iostream>

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

// Group
void Group::attribute(string key, Signal s) {
    for(Drawable *e : elements)
        e->attribute(key, s);
}

void Group::add(Drawable* d) {
    elements.push_back(d);
};

void Group::draw(sf::RenderTarget* target) {
    for(Drawable *e : elements)
        e->draw(target);
};
//

// Polygon
Polygon::Polygon(int n) {
    double r = 1;
    sf_shape = sf::CircleShape(r);
    sf_shape.setPointCount(n);

    sf_shape.setOrigin(r, r);
}

#define check_attribute(__n, __name) \
    if (s.n() == __n && !key.compare(__name))

void Polygon::attribute(string key, Signal s) {
    static const double pi = 3.141592654;
    Color c(s.x(), s.y(), s.z(), s.w());

    check_attribute(1, "line")
        return sf_shape.setOutlineThickness(s.x());

    check_attribute(1, "rotation")
        return sf_shape.rotate(180 *s.x()/pi);

    check_attribute(1, "radius")
        return sf_shape.scale(s.x(), s.x());

    check_attribute(2, "position")
        return sf_shape.setPosition(s.x(), s.y());

    check_attribute(4, "fill")
        return sf_shape.setFillColor(sf::Color(c.r()*255,
                                               c.g()*255,
                                               c.b()*255,
                                               c.a()*255));

    check_attribute(4, "stroke")
        return sf_shape.setOutlineColor(sf::Color(c.r()*255,
                                                  c.g()*255,
                                                  c.b()*255,
                                                  c.a()*255));
}

void Polygon::draw(sf::RenderTarget* target) {
    target->draw(sf_shape);
}
//

// Window
Window::Window(const char* name) {
    sf_window.create(sf::VideoMode(800, 600), name);
}

bool Window::is_open() {
    return sf_window.isOpen();
}

void Window::render(Drawable* child) {
    sf::Event event;

    while (sf_window.pollEvent(event)) {
        if (event.type == sf::Event::Closed)
            sf_window.close();
    }

    sf::View view;
    sf::Vector2<unsigned int> size = sf_window.getSize();
    double w = size.x,
           h = size.y;
    view.setCenter(0, 0);
    view.setSize(2, 2 * h/w);

    sf_window.setView(view);

    sf_window.clear(sf::Color::Black);

    child->draw(&sf_window);

    sf_window.display();
}

Window* Window::memo(const char* name) {
    return memorize<Window>(name);
}
//
