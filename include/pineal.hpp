#include <SFML/Graphics.hpp>
#include <signals.hpp>


class Drawable {
    public:
        virtual void draw(sf::RenderTarget* target, sf::RenderStates states) {};
        virtual ~Drawable() {};
};


class Polygon : public Drawable {
    public:
        Polygon(int);

        void attribute(std::string key, Signal s);
        void apply_all_attributes();
        void apply_attribute(std::string key, Signal s);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    protected:
        sf::CircleShape sf_shape;
        std::map<std::string, Signal> attributes;
};

class Layer : public Drawable {
    public:
        Layer();
        Layer(std::string name);

        void render(Drawable* child);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    private:
        sf::ConvexShape sf_shape;
        sf::RenderTexture render_texture;
        double w, h;
};

class Window {
    public:
        Window(std::string name);
        void render(Drawable* child);

    private:
        sf::RenderWindow render_window;
};

Window*  window(std::string name);
Layer*   layer(std::string name);
Polygon  polygon(int n);

void render(Window* w, Drawable* child);
void render(Layer*  l, Drawable* child);

void attribute(Polygon *p, std::string key, Signal s);
