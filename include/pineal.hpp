#include <SFML/Graphics.hpp>
#include <signals.hpp>

class Entity {
    public:
        void attribute(std::string key, Signal s);
        void apply_all_attributes();
        virtual void apply_attribute(std::string key, Signal s) {};
        virtual ~Entity() {};

    protected:
        std::map<std::string, Signal> attributes;
};

class Drawable : public Entity {
    public:
        virtual void draw(sf::RenderTarget* target, sf::RenderStates states) {};
        virtual ~Drawable() {};
};

class Group : public Drawable {
    public:
        Group() : depth(1) {};

        void add(Drawable* d);
        virtual void apply_attribute(std::string key, Signal s);
        virtual void draw(sf::RenderTarget* target, sf::RenderStates states);

    protected:
        std::vector<Drawable*> elements;
        sf::Transform sf_transform;
        int depth;
};

class Polygon : public Drawable {
    public:
        Polygon(int);

        void apply_attribute(std::string key, Signal s);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    protected:
        sf::CircleShape sf_shape;
};

class Layer : public Drawable {
    public:
        Layer();
        Layer(std::string name);

        void render(Drawable* child);
        void apply_attribute(std::string key, Signal s);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    private:
        sf::ConvexShape sf_shape;
        sf::RenderTexture render_texture;
        double w, h;
};

class Window : public Entity {
    public:
        Window(std::string name);
        void render(Drawable* child);

    private:
        sf::RenderWindow render_window;
};

Window*  window(std::string name);
Layer*   layer(std::string name);
Polygon  polygon(int n);
Group    group();

void render(Window* w, Drawable* child);
void render(Layer*  l, Drawable* child);

void add(Group *g, Drawable* d);

void attribute(Entity *e, std::string key, Signal s);
