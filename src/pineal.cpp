#include <SFML/Graphics.hpp>
#include <pineal.hpp>
#include <memory>
#include <iostream>
static const double pi = 3.141592654;

using namespace std;
//using namespace std::__cxx11;

#define check_attribute(__n, __name, __code) \
    if (s.n() == __n && !key.compare(__name)) { \
        __code; \
        return; \
    }


template<class T, typename K>
T* memorize(K name) {
    // I can not use templates in SWIG interfaces
    static map<K, unique_ptr<T>> memory;

    if (memory.count(name) == 0) {
        memory[name] = unique_ptr<T>(new T(name));
    }
    return memory[name].get();
}


// Polygon
Polygon::Polygon(int n) {
    double r = 1;
    sf_shape = sf::CircleShape(r);
    sf_shape.setPointCount(n);

    sf_shape.setOrigin(r, r);
}

void Polygon::attribute(string key, Signal s) {
    attributes[key] = s;
}

void Polygon::apply_all_attributes() {
    for (const auto& p : attributes) {
        apply_attribute(p.first, p.second);
    }
}

void Polygon::apply_attribute(string key, Signal s) {
    check_attribute(1, "line",
                    sf_shape.setOutlineThickness(s.x()));

    check_attribute(1, "rotation",
                    sf_shape.setRotation(180 * s.x()/pi));

    check_attribute(1, "radius",
                    sf_shape.setScale(s.x(), s.x()));

    check_attribute(2, "position",
                    sf_shape.setPosition(s.x(), s.y()));

    check_attribute(4, "fill",
                    sf_shape.setFillColor(sf::Color(s.x()*255,
                                                    s.y()*255,
                                                    s.z()*255,
                                                    s.w()*255)));

    check_attribute(4, "stroke",
                    sf_shape.setOutlineColor(sf::Color(s.x()*255,
                                                       s.y()*255,
                                                       s.z()*255,
                                                       s.w()*255)));
}

void Polygon::draw(sf::RenderTarget* target, sf::RenderStates states) {
    apply_all_attributes();
    target->draw(sf_shape, states);
}
//

// Layer
Layer::Layer() : w(2000), h(2000) {
    sf_shape = sf::ConvexShape(4);
    render_texture.create(w, h);

    sf_shape.setPoint(0, sf::Vector2f(-1, -1));
    sf_shape.setPoint(1, sf::Vector2f(1, -1));
    sf_shape.setPoint(2, sf::Vector2f(1, 1));
    sf_shape.setPoint(3, sf::Vector2f(-1, 1));
}

Layer::Layer(string name) : Layer() {
}

void Layer::render(Drawable* child) {
    sf::View view;
    view.setCenter(0, 0);
    view.setSize(2, 2);

    render_texture.setView(view);
    render_texture.clear();
    render_texture.setSmooth(true);
    child->draw(&render_texture, sf::RenderStates());
    render_texture.display();
}


void Layer::draw(sf::RenderTarget* target, sf::RenderStates states) {
    const sf::Texture& texture = render_texture.getTexture();
    sf::Sprite sprite(texture);

    sf_shape.setTexture(&texture);
    target->draw(sf_shape, states);
}
//

// Window
Window::Window(string name) {
    render_window.create(sf::VideoMode(800, 600), name);
}

void Window::render(Drawable* child) {
    if (!render_window.isOpen())
        return;

    sf::Event event;

    while (render_window.pollEvent(event)) {
        if (event.type == sf::Event::Closed)
            render_window.close();
    }

    sf::View view;
    sf::Vector2<unsigned int> size = render_window.getSize();
    double w = size.x,
           h = size.y;
    view.setCenter(0, 0);
    view.setSize(2, 2 * h/w);

    render_window.clear(sf::Color::Black);
    render_window.setView(view);

    child->draw(&render_window, sf::RenderStates());
    render_window.display();
}
//

Window* window(std::string name) {
    return memorize<Window>(name);
}

Layer* layer(std::string name) {
    return memorize<Layer>(name);
}

Polygon polygon(int n) {
    return Polygon(n);
}

void render(Window* w, Drawable* child) {
    w->render(child);
}

void render(Layer* l, Drawable* child) {
    l->render(child);
}

void attribute(Polygon *p, std::string key, Signal s) {
    p->attribute(key, s);
}
