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


// Drawable
Drawable::~Drawable() {}

void Drawable::draw(sf::RenderTarget* target) {}
//

// Shape
Shape::~Shape() {}
//

// Surface
Surface::~Surface() {}

void Surface::render(Drawable* child) {}
//

// Polygon
Polygon::Polygon(int n) {
    sf_shape = sf::CircleShape(100);
    sf_shape.setPointCount(n);
    fill(1, 1, 1, 1);
}

// TODO move to Shape::fill()
Shape* Polygon::fill(double r, double g, double b, double a) {
    sf_fill = sf::Color(r*255, g*255, b*255, a*255);
    return new Polygon(*this);
}

void Polygon::draw(sf::RenderTarget* target) {
    sf_shape.setFillColor(sf_fill);
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

    sf_window.clear(sf::Color::Black);

    child->draw(&sf_window);

    sf_window.display();
}

Window* Window::memo(const char* name) {
    return memorize<Window>(name);
}
//

