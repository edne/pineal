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
Shape::~Shape() {}

void Shape::fill(Color c) {
    sf_fill = sf::Color(c.r*255, c.g*255, c.b*255, c.a*255);
}

void Shape::stroke(Color c) {
    sf_stroke = sf::Color(c.r*255, c.g*255, c.b*255, c.a*255);
}

void Shape::line(double t) {
    thickness = t;
}

void Shape::draw(sf::RenderTarget* target) {}
//

// Surface
Surface::~Surface() {}

void Surface::render(Drawable* child) {}
//

// Polygon
Polygon::Polygon(int n) {
    sf_shape = sf::CircleShape(1);
    sf_shape.setPointCount(n);
    sf_shape.setPosition(-1, -1);
    //sf_shape.setOrigin(0, 0);
    //sf_shape.rotate(30);
    fill(Color(1));
    stroke(Color(0));
    line(0);
}

void Polygon::draw(sf::RenderTarget* target) {
    sf_shape.setFillColor(sf_fill);
    sf_shape.setOutlineThickness(thickness);
    sf_shape.setOutlineColor(sf_stroke);
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

