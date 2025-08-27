using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using BertisUtils;

public class UtilsTest
{
    // A Test behaves as an ordinary method
    [Test]
    public void TestAngleFromVectorLength()
    {
        Vector3 res = new Vector3();

        for (int i = 0; i < 5; i++)
        {
            float angle = Random.Range(0.0f, 360.0f);
            res = BertisUtils.VectorUtils.GetVectorFromAngle(angle);
            Assert.AreEqual(1.0f, res.magnitude);
        }
        
    }

    
}
