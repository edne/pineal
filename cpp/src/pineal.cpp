#include <SFML/Graphics.hpp>
#include <pineal.hpp>
#include <memory>
#include <iostream>
static const double pi = 3.141592654;

using namespace std;

#define check_attribute(__n, __name) \
    if (s.n() == __n && !key.compare(__name))


template<class T, typename K>
T* memorize(K name) {
    // I can not use templates in SWIG interfaces
    static map<K, unique_ptr<T>> memory;

    if (memory.count(name) == 0) {
        memory[name] = unique_ptr<T>(new T(name));
    }
    return memory[name].get();
}

// Entity
void Entity::attribute(std::string key, Signal s) {
    attributes[key] = s;
};

void Entity::apply_all_attributes() {
    for (const auto& p : attributes) {
        apply_attribute(p.first, p.second);
    }
}
//

// Group
void Group::apply_attribute(string key, Signal s) {
    for (Drawable *e : elements)
        e->apply_attribute(key, s);
}

void Group::add(Drawable* d) {
    elements.push_back(d);
};

void Group::draw(sf::RenderTarget* target, sf::RenderStates states) {
    apply_all_attributes();
    for (Drawable *e : elements)
        e->draw(target, states);
};
//

// Transf*ormation
void Transform::apply_attribute(string key, Signal s) {
    check_attribute(2, "translate") {
        sf_transform.translate(s.x(), s.y());
        return;
    }

    check_attribute(1, "rotate") {
        sf_transform.rotate(180 * s.x() / pi);
        return;
    }

    check_attribute(1, "scale") {
        sf_transform.scale(s.x(), s.x());
        return;
    }

    check_attribute(2, "scale") {
        sf_transform.scale(s.x(), s.y());
        return;
    }

    for (Drawable *e : elements)
        e->apply_attribute(key, s);
}

void Transform::draw(sf::RenderTarget* target, sf::RenderStates states) {
    sf_transform = sf::Transform();
    apply_all_attributes();

    states.transform *= sf_transform;

    for (Drawable *e : elements) {
        e->draw(target, states);
    }
};
//

// Polygon
Polygon::Polygon(int n) {
    double r = 1;
    sf_shape = sf::CircleShape(r);
    sf_shape.setPointCount(n);

    sf_shape.setOrigin(r, r);
}

void Polygon::apply_attribute(string key, Signal s) {
    Color c(s.x(), s.y(), s.z(), s.w());

    check_attribute(1, "line")
        return sf_shape.setOutlineThickness(s.x());

    check_attribute(1, "rotation")
        return sf_shape.setRotation(180 * s.x()/pi);

    check_attribute(1, "radius")
        return sf_shape.setScale(s.x(), s.x());

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

void Polygon::draw(sf::RenderTarget* target, sf::RenderStates states) {
    apply_all_attributes();
    target->draw(sf_shape, states);
}
//

// Layer
Layer::Layer() : w(2000), h(2000){
    render_texture.create(w, h);
}

void Layer::render(Drawable* child) {
    sf::View view;
    view.setCenter(0, 0);
    view.setSize(2, 2);

    render_texture.setView(view);
    render_texture.clear();
    child->draw(&render_texture, sf::RenderStates());
    render_texture.display();
}

void Layer::draw(sf::RenderTarget* target, sf::RenderStates states) {
    const sf::Texture& texture = render_texture.getTexture();
    sf::Sprite sprite(texture);

    apply_all_attributes();
    sprite.scale(2.0 / w, 2.0 / h);
    sprite.setPosition(-1, -1);
    target->draw(sprite, states);
}
//

// Window
Window::Window(const char* name) {
    render_window.create(sf::VideoMode(800, 600), name);
}

bool Window::is_open() {
    return render_window.isOpen();
}

void Window::render(Drawable* child) {
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

    Layer layer;

    layer.render(child);

    render_window.clear(sf::Color::Black);
    render_window.setView(view);

    layer.draw(&render_window, sf::RenderStates());
    render_window.display();
}

Window* Window::memo(const char* name) {
    return memorize<Window>(name);
}
//
