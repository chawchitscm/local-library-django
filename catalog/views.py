import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.forms import RenewBookModelForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
 
    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_genres' : num_genres,
        'num_visits' : num_visits
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 1

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksByUserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_bookinstance.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instance
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
