package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.service.AssistenteSocialService;
import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/assistente_social")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AssistenteSocialResource {

    @Inject
    AssistenteSocialService service;

    @GET
    public List<AssistenteSocialDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AssistenteSocialDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AssistenteSocialDTO dto) {
        AssistenteSocialDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }
}
