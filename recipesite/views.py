from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Recipe
from .models import Comment
from .forms import CommentForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')

        comment_deleted = False

        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
                "comment_deleted": False
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)

        commented = False
        comment_deleted = False

        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        if 'comment_id' in request.POST:
            comment_id = request.POST['comment_id']

            if 'comment_task' in request.POST:
                comment_task = request.POST['comment_task']

                if comment_task == 'edit':
                    comment_form = CommentForm(instance=Comment.objects.get(id=comment_id), data=request.POST)
                    comment = comment_form.save(commit=False)
                    comment.save()

                elif comment_task == 'delete':
                    comment = get_object_or_404(Comment, id=comment_id)
                    comment.delete()
                    comment_deleted = True

        else:
            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.save()
                commented = True

        comments = recipe.comments.filter(approved=True).order_by('created_on')

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": commented,
                "liked": liked,
                "comment_deleted": comment_deleted,
                "comment_form": CommentForm()
            },
        )


class RecipeLike(View):

    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))
