from typing import List, Optional, Dict, Any
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class Ingredient(BaseModel):
    """Represents a single ingredient item with a name and optional quantity."""
    name: str = Field(..., description="Ingredient name")
    quantity: Optional[str] = Field(None, description="Quantity description (e.g., '2 cups')")


# PUBLIC_INTERFACE
class Recipe(BaseModel):
    """Represents a recipe with details, ingredients, steps, and metadata."""
    id: str = Field(..., description="Unique identifier (UUID as string)")
    title: str = Field(..., description="Recipe title")
    description: str = Field(..., description="Short description of the recipe")
    image_url: Optional[str] = Field(None, description="URL to an image of the recipe")
    ingredients: List[Ingredient] = Field(default_factory=list, description="List of ingredients")
    steps: List[str] = Field(default_factory=list, description="Step-by-step instructions")
    total_time_minutes: int = Field(..., description="Total time required in minutes")
    servings: int = Field(..., description="Number of servings")
    tags: List[str] = Field(default_factory=list, description="List of tags for filtering")


# PUBLIC_INTERFACE
class PaginatedRecipesResponse(BaseModel):
    """Paginated response shape for a recipe list."""
    items: List[Recipe] = Field(..., description="List of recipes in current page")
    total: int = Field(..., description="Total number of recipes")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")


openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and diagnostics."
    },
    {
        "name": "Recipes",
        "description": "Browse, search, and view recipes."
    },
]

app = FastAPI(
    title="Recipe Explorer API",
    description="REST API for browsing and searching recipes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS: allow localhost and common preview origins
allowed_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://localhost",
    "https://localhost:3000",
    "https://localhost:3001",
    # Common preview domains (adjusted to be permissive for demo)
    "https://*.kavia.ai",
    "https://*.cloud.kavia.ai",
    "*",  # For demo purposes; tighten for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex="https://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _mk_id() -> str:
    return str(uuid.uuid4())


def _seed_recipes() -> List[Recipe]:
    """Create a small, varied selection of recipes for demo and search."""
    seed: List[Dict[str, Any]] = [
        dict(
            id=_mk_id(),
            title="Classic Margherita Pizza",
            description="A simple pizza topped with fresh tomatoes, mozzarella, and basil.",
            image_url="https://images.unsplash.com/photo-1548365328-8b0b1a07e2fd?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Pizza dough", "quantity": "1 ball"},
                {"name": "Tomato sauce", "quantity": "1/2 cup"},
                {"name": "Fresh mozzarella", "quantity": "8 oz"},
                {"name": "Fresh basil leaves", "quantity": "Handful"},
                {"name": "Olive oil", "quantity": "1 tbsp"},
            ],
            steps=[
                "Preheat oven to 500°F (260°C).",
                "Stretch the dough on a floured surface.",
                "Spread tomato sauce, add mozzarella slices, drizzle olive oil.",
                "Bake 8–10 minutes until crust is crisp.",
                "Top with basil and serve hot.",
            ],
            total_time_minutes=25,
            servings=2,
            tags=["italian", "vegetarian", "pizza", "quick"],
        ),
        dict(
            id=_mk_id(),
            title="Spicy Thai Basil Chicken",
            description="Savory and spicy stir-fried chicken with Thai basil.",
            image_url="https://images.unsplash.com/photo-1604908554063-f3eccb6b4b91?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Chicken thighs", "quantity": "1 lb, chopped"},
                {"name": "Garlic", "quantity": "4 cloves, minced"},
                {"name": "Red chilies", "quantity": "2, sliced"},
                {"name": "Oyster sauce", "quantity": "2 tbsp"},
                {"name": "Fish sauce", "quantity": "1 tbsp"},
                {"name": "Thai basil", "quantity": "1 cup"},
            ],
            steps=[
                "Heat oil in a wok over high heat.",
                "Stir-fry garlic and chilies until fragrant.",
                "Add chicken and cook through.",
                "Stir in sauces and basil just before serving.",
            ],
            total_time_minutes=20,
            servings=3,
            tags=["thai", "spicy", "stir-fry", "chicken", "quick"],
        ),
        dict(
            id=_mk_id(),
            title="Blueberry Lemon Muffins",
            description="Moist muffins bursting with blueberries and bright lemon zest.",
            image_url="https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "All-purpose flour", "quantity": "2 cups"},
                {"name": "Sugar", "quantity": "3/4 cup"},
                {"name": "Baking powder", "quantity": "2 tsp"},
                {"name": "Milk", "quantity": "3/4 cup"},
                {"name": "Egg", "quantity": "1"},
                {"name": "Blueberries", "quantity": "1 1/2 cups"},
                {"name": "Lemon zest", "quantity": "1 tbsp"},
            ],
            steps=[
                "Preheat oven to 375°F (190°C).",
                "Whisk dry ingredients; combine wet ingredients.",
                "Fold wet into dry, add blueberries and lemon zest.",
                "Fill muffin tin and bake 18–22 minutes.",
            ],
            total_time_minutes=35,
            servings=12,
            tags=["baking", "dessert", "blueberry", "breakfast"],
        ),
        dict(
            id=_mk_id(),
            title="Creamy Tomato Basil Soup",
            description="Comforting soup made with tomatoes, cream, and fresh basil.",
            image_url="https://images.unsplash.com/photo-1551183053-bf91a1d81141?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Canned tomatoes", "quantity": "28 oz"},
                {"name": "Onion", "quantity": "1, chopped"},
                {"name": "Garlic", "quantity": "3 cloves"},
                {"name": "Heavy cream", "quantity": "1/2 cup"},
                {"name": "Fresh basil", "quantity": "1/2 cup"},
            ],
            steps=[
                "Sauté onion and garlic until soft.",
                "Add tomatoes and simmer 15 minutes.",
                "Blend smooth, stir in cream and basil.",
                "Season and serve warm.",
            ],
            total_time_minutes=30,
            servings=4,
            tags=["soup", "vegetarian", "comfort"],
        ),
        dict(
            id=_mk_id(),
            title="Grilled Salmon with Lemon Dill",
            description="Flaky salmon fillets grilled with fresh lemon and dill.",
            image_url="https://images.unsplash.com/photo-1617191518005-c13b39d3f5d3?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Salmon fillets", "quantity": "4"},
                {"name": "Lemon", "quantity": "1, sliced"},
                {"name": "Fresh dill", "quantity": "2 tbsp"},
                {"name": "Olive oil", "quantity": "1 tbsp"},
            ],
            steps=[
                "Preheat grill to medium-high.",
                "Brush salmon with oil, season, top with lemon and dill.",
                "Grill 4–5 minutes per side.",
            ],
            total_time_minutes=18,
            servings=4,
            tags=["seafood", "healthy", "gluten-free"],
        ),
        dict(
            id=_mk_id(),
            title="Veggie Buddha Bowl",
            description="Nourishing bowl with roasted veggies, grains, and tahini dressing.",
            image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Quinoa", "quantity": "1 cup"},
                {"name": "Sweet potato", "quantity": "1, cubed"},
                {"name": "Chickpeas", "quantity": "1 can, drained"},
                {"name": "Spinach", "quantity": "2 cups"},
                {"name": "Tahini", "quantity": "2 tbsp"},
            ],
            steps=[
                "Roast sweet potato and chickpeas at 400°F (205°C) until crisp.",
                "Cook quinoa per package.",
                "Assemble with spinach and drizzle tahini dressing.",
            ],
            total_time_minutes=35,
            servings=2,
            tags=["vegan", "bowl", "healthy", "gluten-free"],
        ),
        dict(
            id=_mk_id(),
            title="Garlic Butter Shrimp Pasta",
            description="Rich and garlicky shrimp tossed with al dente pasta.",
            image_url="https://images.unsplash.com/photo-1473093295043-cdd812d0e601?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Spaghetti", "quantity": "12 oz"},
                {"name": "Shrimp", "quantity": "1 lb, peeled"},
                {"name": "Butter", "quantity": "4 tbsp"},
                {"name": "Garlic", "quantity": "4 cloves, minced"},
                {"name": "Parsley", "quantity": "2 tbsp"},
            ],
            steps=[
                "Cook pasta until al dente.",
                "Sauté garlic in butter, add shrimp and cook until pink.",
                "Toss with pasta and parsley; season to taste.",
            ],
            total_time_minutes=25,
            servings=4,
            tags=["pasta", "seafood", "comfort"],
        ),
        dict(
            id=_mk_id(),
            title="Hearty Beef Chili",
            description="Slow-simmered chili with beans and spices.",
            image_url="https://images.unsplash.com/photo-1481931715705-36f6e3a82b5b?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Ground beef", "quantity": "1 lb"},
                {"name": "Kidney beans", "quantity": "1 can"},
                {"name": "Tomato sauce", "quantity": "1 can"},
                {"name": "Chili powder", "quantity": "2 tbsp"},
                {"name": "Onion", "quantity": "1, diced"},
            ],
            steps=[
                "Brown beef with onions.",
                "Add beans, sauce, and spices.",
                "Simmer 30–45 minutes, stirring occasionally.",
            ],
            total_time_minutes=60,
            servings=6,
            tags=["beef", "stew", "spicy", "comfort"],
        ),
        dict(
            id=_mk_id(),
            title="Avocado Toast with Poached Egg",
            description="Simple and delicious breakfast with creamy avocado and a runny egg.",
            image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Sourdough bread", "quantity": "2 slices"},
                {"name": "Avocado", "quantity": "1, mashed"},
                {"name": "Eggs", "quantity": "2, poached"},
                {"name": "Chili flakes", "quantity": "Pinch"},
            ],
            steps=[
                "Toast bread and spread with mashed avocado.",
                "Top with poached eggs and chili flakes.",
                "Season with salt and pepper.",
            ],
            total_time_minutes=10,
            servings=1,
            tags=["breakfast", "quick", "vegetarian"],
        ),
        dict(
            id=_mk_id(),
            title="Mango Coconut Chia Pudding",
            description="Tropical chia pudding with mango puree and coconut milk.",
            image_url="https://images.unsplash.com/photo-1511914265872-c40672604a66?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Chia seeds", "quantity": "1/4 cup"},
                {"name": "Coconut milk", "quantity": "1 cup"},
                {"name": "Mango", "quantity": "1, pureed"},
                {"name": "Honey", "quantity": "1 tbsp"},
            ],
            steps=[
                "Mix chia seeds with coconut milk and honey.",
                "Chill for 2 hours until set.",
                "Top with mango puree and serve.",
            ],
            total_time_minutes=10,
            servings=2,
            tags=["dessert", "vegan", "tropical", "no-bake"],
        ),
        dict(
            id=_mk_id(),
            title="Roasted Herb Chicken",
            description="Juicy whole roasted chicken with fragrant herbs.",
            image_url="https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1200&auto=format&fit=crop",
            ingredients=[
                {"name": "Whole chicken", "quantity": "1"},
                {"name": "Butter", "quantity": "3 tbsp"},
                {"name": "Mixed herbs", "quantity": "2 tbsp"},
                {"name": "Lemon", "quantity": "1"},
            ],
            steps=[
                "Preheat oven to 425°F (220°C).",
                "Rub chicken with butter and herbs.",
                "Roast 60–75 minutes until internal temp is 165°F (74°C).",
                "Rest before carving.",
            ],
            total_time_minutes=90,
            servings=6,
            tags=["chicken", "roast", "family"],
        ),
    ]
    return [Recipe(**r) for r in seed]


RECIPES: List[Recipe] = _seed_recipes()
RECIPES_BY_ID: Dict[str, Recipe] = {r.id: r for r in RECIPES}


def _match_query(recipe: Recipe, q: str) -> bool:
    """Case-insensitive substring match on title and tags."""
    ql = q.lower()
    if ql in recipe.title.lower():
        return True
    for tag in recipe.tags:
        if ql in tag.lower():
            return True
    return False


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Returns service status for health monitoring.",
)
def health_check() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        JSON object with service status.
    """
    return {"status": "ok"}


@app.get(
    "/recipes",
    response_model=PaginatedRecipesResponse,
    tags=["Recipes"],
    summary="List recipes",
    description="Returns a paginated list of recipes. Optional search by query over title and tags (case-insensitive substring).",
)
def list_recipes(
    q: Optional[str] = Query(None, description="Search query over title and tags (case-insensitive substring)"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> PaginatedRecipesResponse:
    """List recipes with optional fuzzy search and pagination.

    Args:
        q: Optional search query string.
        page: Page number (1-indexed).
        page_size: Number of items per page.

    Returns:
        PaginatedRecipesResponse with items and metadata.
    """
    items = RECIPES
    if q:
        items = [r for r in RECIPES if _match_query(r, q)]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = items[start:end]

    return PaginatedRecipesResponse(
        items=paginated,
        total=total,
        page=page,
        page_size=page_size,
    )


@app.get(
    "/recipes/{recipe_id}",
    response_model=Recipe,
    tags=["Recipes"],
    summary="Get a recipe",
    description="Retrieve a single recipe by its ID.",
)
def get_recipe(recipe_id: str) -> Recipe:
    """Retrieve recipe by ID.

    Args:
        recipe_id: Recipe UUID (string).

    Returns:
        A Recipe model.

    Raises:
        HTTPException: 404 if not found.
    """
    recipe = RECIPES_BY_ID.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
