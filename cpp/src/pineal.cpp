#include <SFML/Graphics.hpp>
#include <pineal.hpp>
#include <memory>

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


// Color
Color::Color(double r, double g, double b, double a)
    : r(r), g(g), b(b), a(a) {}

Color::Color(double r, double g, double b)
    : Color(r, g, b, 1) {}

Color::Color(double x, double a)
    : Color(x, x, x, a) {}

Color::Color(double x)
    : Color(x, x, x, 1) {}
//


// Drawable
Drawable::~Drawable() {}

void Drawable::draw(sf::RenderTarget* target) {}
//

// Shape
//

// Surface
Surface::~Surface() {}

void Surface::render(Drawable* child) {}
//

// Polygon
Polygon::Polygon(int n) {
    double r = 1;
    sf_shape = sf::CircleShape(r);
    sf_shape.setPointCount(n);

    sf_shape.setOrigin(r, r);

    fill(Color(1));
    stroke(Color(0));
    line(0);
}

void Polygon::fill(Color c) {
    sf_shape.setFillColor(sf::Color(c.r*255, c.g*255, c.b*255, c.a*255));
}

void Polygon::stroke(Color c) {
    sf_shape.setOutlineColor(sf::Color(c.r*255, c.g*255, c.b*255, c.a*255));
}

void Polygon::line(double thickness) {
    sf_shape.setOutlineThickness(thickness);
}

void Polygon::draw(sf::RenderTarget* target) {
    target->draw(sf_shape);
}

void Polygon::position(double x, double y) {
    sf_shape.setPosition(x, y);
}

void Polygon::rotate(double t) {
    static const double pi = 3.141592654;
    sf_shape.rotate(180 * t/pi);
}

void Polygon::scale(double x, double y) {
    sf_shape.scale(x, y);
}

void Polygon::scale(double r) {
    sf_shape.scale(r, r);
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

