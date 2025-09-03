using ExplodotechUtils;
using UnityEngine;
using System.Collections.Generic;

public class Emitter : MonoBehaviour
{
    public float signalStrength = 1.0f;
    private EmitterGeneric emitter;

    public TextAsset jsonProfile;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {

        if (jsonProfile == null)
        {
            Debug.LogError("JSON profile not assigned to the Emitter!");
            return;
        }

        SpectrumProfile profile = JsonUtility.FromJson<SpectrumProfile>(jsonProfile.text);
        emitter = new EmitterGeneric(profile);

    }

    // Update is called once per frame
    void Update()
    {

    }

    public float GetSignalStrength()
    {
        return this.signalStrength;
    }

    public Dictionary<EM_Spectrum, float> GetEmissionProfile()
    {
        return emitter.GetEmissionProfile();
    }
}
