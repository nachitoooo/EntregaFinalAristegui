
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages  # Importa la biblioteca de mensajes
from .models import CanalMensaje, CanalUsuario, Canal
from django.http import HttpResponse, Http404, JsonResponse
from .forms import FormMensajes, SeleccionarDestinatarioForm
from django.views.generic.edit import FormMixin
from django.views.generic import View

class Inbox(View):
    def get(self, request):
        inbox = Canal.objects.filter(
            canalusuario__usuario__in=[request.user.id])
        form = FormMensajes()
        seleccionar_usuarios_form = SeleccionarDestinatarioForm()

        context = {
            "inbox": inbox,
            "form": form,
            "seleccionar_usuarios": seleccionar_usuarios_form,
        }

        return render(request, 'inbox.html', context)

    def post(self, request):
        seleccionar_usuarios_form = SeleccionarDestinatarioForm(request.POST)

        if seleccionar_usuarios_form.is_valid():
            destinatario = seleccionar_usuarios_form.cleaned_data['destinatario']

            return redirect('detailms', username=destinatario.username)

        inbox = Canal.objects.filter(
            canalusuario__usuario__in=[request.user.id])
        context = {
            "inbox": inbox,
            "seleccionar_usuarios": seleccionar_usuarios_form,
        }
        return render(request, 'inbox.html', context)

class CanalFormMixin(FormMixin):
	form_class =FormMensajes

	def get_success_url(self):
		return self.request.path

	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			raise PermissionDenied

		form = self.get_form()
		if form.is_valid():
			canal = self.get_object()
			usuario = self.request.user 
			mensaje = form.cleaned_data.get("mensaje")
			canal_obj = CanalMensaje.objects.create(canal=canal, usuario=usuario, texto=mensaje)
			
			return super().form_valid(form)

		else:
			
			return super().form_invalid(form)


class CanalDetailView(LoginRequiredMixin, DetailView):
    template_name = 'canal_detail.html'
    queryset = Canal.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        obj = context['object']
        context['si_canal_miembro'] = self.request.user in obj.usuarios.all()
        context['form'] = FormMensajes()

        return context

    def post(self, request, *args, **kwargs):
        form = FormMensajes(request.POST)
        if form.is_valid():
            canal = self.get_object()
            usuario = self.request.user
            mensaje = form.cleaned_data.get("mensaje")
            CanalMensaje.objects.create(
                canal=canal, usuario=usuario, texto=mensaje)

        return redirect('canal-detail', pk=kwargs['pk'])


class DetailMs(LoginRequiredMixin, CanalFormMixin, DetailView):

	template_name = 'canal_detail.html'



	def get_object(self, *args, **kwargs):

		username = self.kwargs.get("username")
		mi_username = self.request.user.username
		canal, _ = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

		if username == mi_username:
			mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)

			return mi_canal

		if canal == None:
			raise Http404

		return canal

def mensajes_privados(request, username, *args, **kwargs):

	if not request.user.is_authenticated:
		return HttpResponse("Prohibido")

	mi_username = request.user.username

	canal, created = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

	if created:
		print("Si, fue creado")

	Usuarios_Canal = canal.canalusuario_set.all().values("usuario__username")
	print(Usuarios_Canal)
	mensaje_canal  = canal.canalmensaje_set.all()
	print(mensaje_canal.values("texto"))

	return HttpResponse(f"Nuestro Id del Canal - {canal.id}")