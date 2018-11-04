// Copyright (C) 2002-2005 Nikolaus Gebhardt
// This file is part of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#include "IrrCompileConfig.h"
#ifdef _IRR_COMPILE_WITH_OPENGL_

#include "COpenGLShaderMaterialRenderer.h"
#include "IGPUProgrammingServices.h"
#include "IShaderConstantSetCallBack.h"
#include "IVideoDriver.h"
#include "os.h"
#define GL_GLEXT_LEGACY 1
#include "glext.h"
#include "COpenGLDriver.h"
#include <stdio.h>
#include <string.h>

namespace irr
{
namespace video
{


//! Constructor
COpenGLShaderMaterialRenderer::COpenGLShaderMaterialRenderer(video::COpenGLDriver* driver, 
	s32& outMaterialTypeNr, const c8* vertexShaderProgram, const c8* pixelShaderProgram,
	IShaderConstantSetCallBack* callback, IMaterialRenderer* baseMaterial, s32 userData)
	: Driver(driver), BaseMaterial(baseMaterial), CallBack(callback),
		VertexShader(0), PixelShader(0), UserData(userData)
{
	if (BaseMaterial)
		BaseMaterial->grab();

	if (CallBack)
		CallBack->grab();

	init(outMaterialTypeNr, vertexShaderProgram, pixelShaderProgram, EVT_STANDARD);
}


//! constructor only for use by derived classes who want to
//! create a fall back material for example.
COpenGLShaderMaterialRenderer::COpenGLShaderMaterialRenderer(COpenGLDriver* driver,
							IShaderConstantSetCallBack* callback,
							IMaterialRenderer* baseMaterial, s32 userData)
: Driver(driver), BaseMaterial(baseMaterial), CallBack(callback),
		VertexShader(0), PixelShader(0), UserData(userData)
{
	if (BaseMaterial)
		BaseMaterial->grab();

	if (CallBack)
		CallBack->grab();
}


//! Destructor
COpenGLShaderMaterialRenderer::~COpenGLShaderMaterialRenderer()
{
	if (CallBack)
		CallBack->drop();

	if (VertexShader)
		Driver->extGlDeleteProgramsARB(1, &VertexShader);

	if (PixelShader)
		Driver->extGlDeleteProgramsARB(1, &PixelShader);

	if (BaseMaterial)
		BaseMaterial->drop ();
}

void COpenGLShaderMaterialRenderer::init(s32& outMaterialTypeNr, const c8* vertexShaderProgram, 
	const c8* pixelShaderProgram, E_VERTEX_TYPE type)
{
	outMaterialTypeNr = -1;

	// create vertex shader
	if (!createVertexShader(vertexShaderProgram))
		return;

	// create pixel shader
	if (!createPixelShader(pixelShaderProgram))
		return;

	// register myself as new material
	outMaterialTypeNr = Driver->addMaterialRenderer(this);
}

bool COpenGLShaderMaterialRenderer::OnRender(IMaterialRendererServices* service, E_VERTEX_TYPE vtxtype)
{
	// call callback to set shader constants
	if (CallBack && (VertexShader || PixelShader))
		CallBack->OnSetConstants(service, UserData);

	return true;
}


void COpenGLShaderMaterialRenderer::OnSetMaterial(video::SMaterial& material, const video::SMaterial& lastMaterial,
	bool resetAllRenderstates, video::IMaterialRendererServices* services)
{
	if (material.MaterialType != lastMaterial.MaterialType || resetAllRenderstates)
	{
		if (VertexShader)
		{
			// set new vertex shader
			Driver->extGlBindProgramARB(GL_VERTEX_PROGRAM_ARB, VertexShader);
			glEnable(GL_VERTEX_PROGRAM_ARB);
		}

		// set new pixel shader
		if (PixelShader)
		{
			Driver->extGlBindProgramARB(GL_FRAGMENT_PROGRAM_ARB, PixelShader);
			glEnable(GL_FRAGMENT_PROGRAM_ARB);
		}

		if (BaseMaterial)
			BaseMaterial->OnSetMaterial(material, material, true, services);
	}

	services->setBasicRenderStates(material, lastMaterial, resetAllRenderstates);
}


void COpenGLShaderMaterialRenderer::OnUnsetMaterial()
{
	// disable vertex shader
	if (VertexShader)
		glDisable(GL_VERTEX_PROGRAM_ARB);

	if (PixelShader)
		glDisable(GL_FRAGMENT_PROGRAM_ARB);

	if (BaseMaterial)
		BaseMaterial->OnUnsetMaterial();
}

//! Returns if the material is transparent.
bool COpenGLShaderMaterialRenderer::isTransparent()
{
	return BaseMaterial ? BaseMaterial->isTransparent() : false; 
}

bool COpenGLShaderMaterialRenderer::createPixelShader(const c8* pxsh)
{
	if (!pxsh)
		return true;

	Driver->extGlGenProgramsARB(1, &PixelShader);
	Driver->extGlBindProgramARB(GL_FRAGMENT_PROGRAM_ARB, PixelShader);

	// clear error buffer
	while(glGetError() != GL_NO_ERROR)	{}

	// compile
	Driver->extGlProgramStringARB(GL_FRAGMENT_PROGRAM_ARB, GL_PROGRAM_FORMAT_ASCII_ARB, 
		strlen(pxsh), pxsh);

	GLenum g = glGetError();
	if (g != GL_NO_ERROR)
	{
		GLint errPos;
		glGetIntegerv( GL_PROGRAM_ERROR_POSITION_ARB, &errPos );

		const GLubyte* errString = glGetString(GL_PROGRAM_ERROR_STRING_ARB);

		char tmp[2048];
		sprintf(tmp, "Pixel shader compilation failed at position %d:\n%s", errPos, errString);
		os::Printer::log(tmp);

		return false;
	}

	return true;
}

bool COpenGLShaderMaterialRenderer::createVertexShader(const char* vtxsh)
{
	if (!vtxsh)
		return true;

	Driver->extGlGenProgramsARB(1, &VertexShader);
	Driver->extGlBindProgramARB(GL_VERTEX_PROGRAM_ARB, VertexShader);

	// clear error buffer
	while(glGetError() != GL_NO_ERROR)	{}

	// compile
	Driver->extGlProgramStringARB(GL_VERTEX_PROGRAM_ARB, GL_PROGRAM_FORMAT_ASCII_ARB, 
		strlen(vtxsh), vtxsh);

	GLenum g = glGetError();
	if (g != GL_NO_ERROR)
	{
		GLint errPos;
		glGetIntegerv( GL_PROGRAM_ERROR_POSITION_ARB, &errPos );

		const GLubyte* errString = glGetString(GL_PROGRAM_ERROR_STRING_ARB);

		char tmp[2048];
		sprintf(tmp, "Vertex shader compilation failed at position %d:\n%s", errPos, errString);
		os::Printer::log(tmp);

		return false;
	}

	return true;	
}


} // end namespace video
} // end namespace irr


#endif

